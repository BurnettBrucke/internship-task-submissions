from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from gateway_service.app.core.config import settings


security = HTTPBearer()


def create_service_token() -> str:
    """Create a JWT token for Gateway -> Processing communication."""

    payload = {
        "service": settings.gateway_service_client_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm="HS256",
    )

    return token


def decode_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify the incoming user's JWT."""

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    username = payload.get("sub")
    user_id = payload.get("user_id")
    role = payload.get("role")

    if not username or not user_id or not role:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return payload