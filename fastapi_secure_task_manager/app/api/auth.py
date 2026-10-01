# ============================================================
# AUTHENTICATION API ROUTES
# ============================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    CurrentUserResponse,
)

from app.services.auth_service import (
    register_user,
    login_user,
)

from app.dependencies.auth import get_current_user

from app.repositories.task_repository import (
    get_user_by_username,
)

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
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user in PostgreSQL.
    """

    try:
        return await register_user(
            db=db,
            user=user,
        )

    except ValueError as e:
        raise conflict_error(str(e))


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate user using PostgreSQL.
    """

    try:
        return await login_user(
            db=db,
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
    db: AsyncSession = Depends(get_db),
):
    """
    Return the currently authenticated user's details.
    """

    username = current_user["sub"]

    user = await get_user_by_username(
        db,
        username=username,
    )

    if user is None:
        raise unauthorized_error("User not found")

    return {
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }