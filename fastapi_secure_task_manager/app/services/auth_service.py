from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import (
    create_user,
    get_user_by_username,
)


async def register_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    role: str,
):
    existing_user = await get_user_by_username(db, username)

    if existing_user:
        return None

    password_hash = hash_password(password)

    return await create_user(
        db=db,
        username=username,
        email=email,
        password_hash=password_hash,
        role=role,
    )


async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
):
    user = await get_user_by_username(db, username)

    if not user:
        return None

    now = datetime.now(timezone.utc)

    # Check temporary block
    if user.blocked_until and now < user.blocked_until:
        return "blocked"

    # Block period has expired
    if user.blocked_until and now >= user.blocked_until:
        user.failed_login_attempts = 0
        user.blocked_until = None

    # Check password
    if not verify_password(password, user.password_hash):
        user.failed_login_attempts += 1

        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            user.blocked_until = now + timedelta(minutes=5)

            await db.commit()

            return "blocked"

        await db.commit()

        return None

    # Successful login
    user.failed_login_attempts = 0
    user.blocked_until = None

    await db.commit()

    return user


def create_user_token(user):
    return create_access_token(
        username=user.username,
        role=user.role,
    )