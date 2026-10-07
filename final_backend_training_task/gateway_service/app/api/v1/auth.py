from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login_user(
    data: LoginRequest,
):
    if (
        data.username != settings.jwt_demo_username
        or data.password != settings.jwt_demo_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    access_token = create_access_token(
        user_id=data.username,
        role="user",
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=(settings.jwt_access_token_expire_minutes * 60),
    )
