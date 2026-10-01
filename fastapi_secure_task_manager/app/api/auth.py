from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_user,
    find_user_by_email,
    find_user_by_username,
    is_login_blocked,
    record_failed_login,
    reset_login_attempts,
    update_last_login,
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
async def register_user(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_db),
):
    existing_username = await find_user_by_username(
        session,
        data.username,
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    existing_email = await find_user_by_email(
        session,
        data.email,
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    try:
        user = await create_user(
            session=session,
            username=data.username,
            email=data.email,
            password=data.password,
            role="user"
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists.",
        )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login_user(
    data: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    if is_login_blocked(data.username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Try again later.",
        )

    user = await authenticate_user(
        session=session,
        username=data.username,
        password=data.password,
    )

    if user is None:
        record_failed_login(data.username)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    reset_login_attempts(data.username)

    await update_last_login(
        session,
        user,
    )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_minutes * 60,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user=Depends(get_current_user),
):
    return current_user