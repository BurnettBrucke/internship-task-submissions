from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth_service import (
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(
            (User.username == request.username)
            | (User.email == request.email)
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "USER_ALREADY_EXISTS",
                "message": "Username or email already exists",
            },
        )

    user = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(
            User.username == request.username
        )
    )

    user = result.scalar_one_or_none()

    if not user or not verify_password(
        request.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid username or password",
            },
        )

    token = create_access_token(
        user_id=user.id,
        username=user.username,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }