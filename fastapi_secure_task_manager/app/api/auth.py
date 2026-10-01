from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException
from app.core.login_security import (
    is_locked,
    record_failed_attempt,
    reset_failed_attempts,
)
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_user,
    generate_token,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await create_user(db, user_data)

    if user is None:
        raise AppException(
            status_code=409,
            code="USERNAME_ALREADY_EXISTS",
            message="Username already exists.",
        )

    await db.commit()

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    username = login_data.username

    # Day 6: account lock protection
    if is_locked(username):
        raise AppException(
            status_code=401,
            code="ACCOUNT_LOCKED",
            message="Too many failed login attempts. Try again later.",
        )

    user = await authenticate_user(
        db,
        username,
        login_data.password,
    )

    # Day 6: invalid credentials protection
    if user is None:
        record_failed_attempt(username)

        raise AppException(
            status_code=401,
            code="INVALID_CREDENTIALS",
            message="Invalid username or password.",
        )

    # Day 6: successful login clears failed attempts
    reset_failed_attempts(username)

    token = generate_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 30 * 60,
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: dict = Depends(get_current_user),
):
    return current_user