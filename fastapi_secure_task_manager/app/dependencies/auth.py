from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException
from app.core.security import decode_access_token
from app.db.database import get_db
from app.services.auth_service import get_user_by_id


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: AsyncSession = Depends(get_db),
):
    if credentials is None:
        raise AppException(
            status_code=401,
            code="AUTHENTICATION_REQUIRED",
            message="Authentication token is required.",
        )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid or expired token.",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid token.",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid token.",
        )

    user = await get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="User associated with token was not found.",
        )

    return user