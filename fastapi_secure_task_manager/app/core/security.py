# ============================================================
# 1. IMPORTS
# ============================================================

from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash

from app.core.config import settings


# ============================================================
# 2. PASSWORD HASHING
# ============================================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure hash.
    """

    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against its stored hash.
    """

    return password_hash.verify(password, hashed_password)


# ============================================================
# 3. CREATE ACCESS TOKEN
# ============================================================

def create_access_token(
    username: str,
    role: str,
) -> str:
    """
    Create a JWT access token.

    The token contains:
    - username
    - role
    - expiration time
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


# ============================================================
# 4. DECODE / VERIFY ACCESS TOKEN
# ============================================================

def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.
    """

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    return payload