from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def create_user(
    db: AsyncSession,
    *,
    username: str,
    email: str,
    password_hash: str,
    role: str = "user",
) -> User:
    """
    Create a new user in PostgreSQL.

    Password hashing is handled by the service/security layer.
    The repository only persists the already-hashed password.
    """

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role=role,
        is_active=True,
    )

    db.add(user)

    # Send INSERT to PostgreSQL but don't commit yet.
    await db.flush()

    # Load database-generated values such as id and created_at.
    await db.refresh(user)

    return user


async def get_user_by_id(
    db: AsyncSession,
    user_id: int,
) -> User | None:
    """
    Retrieve a user by primary key.
    """

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    return result.scalar_one_or_none()


async def get_user_by_username(
    db: AsyncSession,
    username: str,
) -> User | None:
    """
    Retrieve a user using the username.
    """

    result = await db.execute(
        select(User).where(
            User.username == username
        )
    )

    return result.scalar_one_or_none()


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    """
    Retrieve a user using the unique email address.
    """

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    return result.scalar_one_or_none()