from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories import user_repository
from app.schemas.user import UserCreate


def user_to_dict(user) -> dict:
    """
    Convert SQLAlchemy User object into the dictionary
    format used by the existing Day 6 authentication flow.
    """
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }


async def get_user_by_username(
    db: AsyncSession,
    username: str,
):
    user = await user_repository.get_user_by_username(
        db,
        username,
    )

    if user is None:
        return None

    return user_to_dict(user)


async def get_user_by_id(
    db: AsyncSession,
    user_id: int,
):
    user = await user_repository.get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        return None

    return user_to_dict(user)


async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
):
    # Check username
    existing_user = await user_repository.get_user_by_username(
        db,
        user_data.username,
    )

    if existing_user is not None:
        return None

    # Check email
    existing_email = await user_repository.get_user_by_email(
        db,
        str(user_data.email),
    )

    if existing_email is not None:
        return None

    password_hash = hash_password(
        user_data.password
    )

    user = await user_repository.create_user(
        db,
        username=user_data.username,
        email=str(user_data.email),
        password_hash=password_hash,
        role=user_data.role,
    )

    return user_to_dict(user)


async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
):
    user = await user_repository.get_user_by_username(
        db,
        username,
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user_to_dict(user)


def generate_token(user: dict) -> str:
    """
    Keep the existing Day 6 JWT payload structure.
    """
    return create_access_token(
        user_id=user["id"],
        username=user["username"],
        role=user["role"],
    )