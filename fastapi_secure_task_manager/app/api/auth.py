from fastapi import APIRouter, Depends, status

from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    CurrentUserResponse,
)

from app.services.auth_service import register_user, login_user
from app.dependencies.auth import get_current_user
from app.data.store import users_db

from app.core.errors import (
    conflict_error,
    unauthorized_error,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserCreate):

    try:
        return register_user(user)

    except ValueError as e:
        raise conflict_error(str(e))


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(login_data: LoginRequest):

    try:
        return login_user(
            username=login_data.username,
            password=login_data.password,
        )

    except ValueError as e:
        raise unauthorized_error(str(e))


# ============================================================
# CURRENT USER
# ============================================================

@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
async def get_me(
    current_user: dict = Depends(get_current_user),
):

    username = current_user["sub"]

    user = users_db.get(username)

    if user is None:
        raise unauthorized_error("User not found")

    return {
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
    }