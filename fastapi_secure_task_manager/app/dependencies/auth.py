from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import decode_access_token
from app.core.errors import unauthorized_error


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

    except Exception:
        raise unauthorized_error(
            "Invalid or expired token"
        )

    username = payload.get("sub")
    role = payload.get("role")

    if not username or not role:
        raise unauthorized_error(
            "Invalid token"
        )

    return payload