from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from gateway_service.app.core.config import settings
from gateway_service.app.core.database import get_db_session
from gateway_service.app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    UserRegisterRequest,
)
from gateway_service.app.services.auth_service import auth_service


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: UserRegisterRequest,
    session: AsyncSession = Depends(get_db_session),
):
    user = await auth_service.register_user(
        session=session,
        username=request.username,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    return {
        "message": "User registered successfully",
        "username": user["username"],
        "role": user["role"],
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
):
    user = await auth_service.verify_user(
        session=session,
        username=request.username,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    payload = {
        "sub": user["username"],
        "user_id": user["id"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm="HS256",
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }