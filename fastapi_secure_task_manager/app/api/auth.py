from fastapi import APIRouter, Depends, status

from app.core.errors import AppException

from app.dependencies.auth import get_current_user
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_user,
    generate_token,
)

from app.core.login_security import (
    is_locked,
    record_failed_attempt,
    reset_failed_attempts,
)




router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user_data: UserCreate):

    user = create_user(user_data)

    if user is None:
      raise AppException(
        status_code=409,
        code="USERNAME_ALREADY_EXISTS",
        message="Username already exists."
      )

    return user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(login_data: LoginRequest):

    username = login_data.username

    # Check whether the user is locked
    if is_locked(username):
        raise AppException(
            status_code=401,
            code="ACCOUNT_LOCKED",
            message="Too many failed login attempts. Try again later."
        )

    user = authenticate_user(
        username,
        login_data.password
    )

    # Invalid username or password
    if user is None:
        record_failed_attempt(username)

        raise AppException(
            status_code=401,
            code="INVALID_CREDENTIALS",
            message="Invalid username or password."
        )

    # Successful login → clear failed attempts
    reset_failed_attempts(username)

    token = generate_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 30 * 60
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: dict = Depends(get_current_user)
):
    return current_user