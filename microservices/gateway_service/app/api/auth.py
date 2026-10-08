from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.core.security import hash_password, verify_password
from fastapi import APIRouter, HTTPException, status, Depends
from jose import jwt
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.username == payload.username)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="user",
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.username == payload.username)
    )

    user = result.scalar_one_or_none()

    if user is None or not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    token_payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": expire,
    }

    access_token = jwt.encode(
        token_payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }