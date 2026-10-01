from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository

from app.core.config import settings

login_attempts: dict[str, dict] = {}


async def find_user_by_username(
    session: AsyncSession,
    username: str,
) -> User | None:
    repository = UserRepository(session)

    return await repository.get_by_username(username)


async def find_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    repository = UserRepository(session)

    return await repository.get_by_id(user_id)


async def find_user_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    repository = UserRepository(session)

    return await repository.get_by_email(email)


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    password: str,
    role: str,
) -> User:
    repository = UserRepository(session)

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=role,
        is_active=True,
    )

    await repository.add(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise

    await session.refresh(user)

    return user


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> User | None:
    user = await find_user_by_username(
        session,
        username,
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user


async def update_last_login(
    session: AsyncSession,
    user: User,
) -> User:
    user.last_login_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(user)

    return user


def is_login_blocked(username: str) -> bool:
    attempt_data = login_attempts.get(username)

    if not attempt_data:
        return False

    blocked_until = attempt_data.get("blocked_until")

    if blocked_until is None:
        return False

    if datetime.now(timezone.utc) < blocked_until:
        return True

    login_attempts.pop(username, None)

    return False


def record_failed_login(username: str) -> None:
    attempt_data = login_attempts.get(
        username,
        {
            "count": 0,
            "blocked_until": None,
        },
    )

    attempt_data["count"] += 1

    if attempt_data["count"] >= settings.max_login_attempts:
        attempt_data["blocked_until"] = (
            datetime.now(timezone.utc)
            + timedelta(minutes=settings.block_duration_minutes)
        )

    login_attempts[username] = attempt_data


def reset_login_attempts(username: str) -> None:
    login_attempts.pop(username, None)