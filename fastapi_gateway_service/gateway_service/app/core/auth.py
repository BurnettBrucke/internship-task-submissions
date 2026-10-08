from datetime import datetime, timedelta, timezone

from app.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm

security = HTTPBearer()


def create_access_token(
    user_id: int,
    username: str,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        if not payload.get("sub"):
            raise JWTError()

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid or expired token",
            },
        )

    return payload