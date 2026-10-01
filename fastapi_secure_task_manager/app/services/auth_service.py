# ============================================================
# AUTH SERVICE
# ============================================================
# Authentication business logic.
#
# Day 7:
# PostgreSQL is now the source of truth for users.
#
# Day 6 functionality preserved:
# - Password hashing
# - Password verification
# - JWT generation
# - User roles
# - Login attempt protection
# ============================================================

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.repositories.task_repository import get_user_by_username
from app.schemas.user import UserCreate
from app.data.store import login_attempts

# ============================================================
# REGISTER USER
# ============================================================

async def register_user(
    db: AsyncSession,
    user: UserCreate,
) -> dict:
    """
    Register a new user in PostgreSQL.
    """

    # Check whether username already exists.
    existing_user = await get_user_by_username(
        db,
        username=user.username,
    )

    if existing_user is not None:
        raise ValueError("Username already exists")

    # Check email separately.
    from sqlalchemy import select

    result = await db.execute(
        select(User).where(User.email == str(user.email))
    )

    existing_email = result.scalar_one_or_none()

    if existing_email is not None:
        raise ValueError("Email already exists")

    # Hash password before storing it.
    password_hash = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=str(user.email),
        password_hash=password_hash,
        role=user.role.value,
        is_active=True,
    )

    db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)

    except Exception:
        await db.rollback()
        raise

    return {
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role,
    }


# ============================================================
# LOGIN USER
# ============================================================

async def login_user(
    db: AsyncSession,
    username: str,
    password: str,
) -> dict:
    """
    Authenticate a user using PostgreSQL.
    """

    user = await get_user_by_username(
        db,
        username=username,
    )

    # --------------------------------------------------------
    # Check login attempts
    # --------------------------------------------------------

    if login_attempts.get(username, 0) >= settings.MAX_LOGIN_ATTEMPTS:
        raise ValueError(
            "Too many failed login attempts. "
            "Please try again later."
        )

    # --------------------------------------------------------
    # User not found
    # --------------------------------------------------------

    if user is None:
        login_attempts[username] = (
            login_attempts.get(username, 0) + 1
        )

        raise ValueError(
            "Invalid username or password"
        )

    # --------------------------------------------------------
    # Check active status
    # --------------------------------------------------------

    if not user.is_active:
        raise ValueError("User account is inactive")

    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    if not verify_password(
        password,
        user.password_hash,
    ):
        login_attempts[username] = (
            login_attempts.get(username, 0) + 1
        )

        raise ValueError(
            "Invalid username or password"
        )

    # --------------------------------------------------------
    # Successful login
    # --------------------------------------------------------

    login_attempts[username] = 0

    user.last_login_at = datetime.utcnow()

    try:
        await db.commit()
        await db.refresh(user)

    except Exception:
        await db.rollback()
        raise

    # --------------------------------------------------------
    # Create JWT
    # --------------------------------------------------------

    access_token = create_access_token(
        username=user.username,
        role=user.role,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800,
    }