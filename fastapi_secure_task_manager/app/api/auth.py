from fastapi import APIRouter , HTTPException , status

from fastapi import Depends
from app.dependencies.auth import get_current_user

from app.core.config import settings
from app.schemas.auth import RegisterRequest , LoginRequest , TokenResponse
from app.core.security import create_access_token

from app.schemas.user import UserResponse
from app.services.auth_service import (
    create_user,
    find_user_by_username,
    authenticate_user,
    is_login_blocked,
    record_failed_login,
    reset_login_attempts,
)
router = APIRouter(prefix="/api/v1/auth" , tags=["Authentication"],)

@router.post("/register" , response_model=UserResponse , status_code= status.HTTP_201_CREATED,)
def register_user(data: RegisterRequest):
    existing_user = find_user_by_username(data.username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    user = create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role,
    )

    return user

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(data: LoginRequest):

    # Check whether the account is temporarily blocked
    if is_login_blocked(data.username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Try again later.",
        )

    user = authenticate_user(
        username=data.username,
        password=data.password,
    )

    # Wrong username/password
    if not user:
        record_failed_login(data.username)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    # Successful login -> reset failed attempts
    reset_login_attempts(data.username)

    access_token = create_access_token(
        user_id=user["id"],
        role=user["role"],
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
def get_me(current_user=Depends(get_current_user)):
    return current_user