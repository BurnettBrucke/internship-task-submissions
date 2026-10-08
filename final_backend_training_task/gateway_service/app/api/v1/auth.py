from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.password import hash_password, verify_password
from app.core.security import create_access_token
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.core.password import hash_password
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    existing_user = await session.scalar(
        select(User).where(User.username == payload.username)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        created_at=datetime.now(timezone.utc),
    )

    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from None

    return RegisterResponse(
        id=user.id,
        username=user.username,
        created_at=user.created_at.isoformat(),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login_user(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    # Find user in user_db
    result = await session.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar_one_or_none()

    # Same response for unknown user and wrong password
    if user is None or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    # JWT now contains the real database user ID
    access_token = create_access_token(
        user_id=str(user.id),
        role="user",
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=(
            settings.jwt_access_token_expire_minutes * 60
        ),
    )