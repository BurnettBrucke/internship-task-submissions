# ============================================================
# 1. IMPORTS
# ============================================================

from pydantic import BaseModel, Field


# ============================================================
# 2. LOGIN REQUEST
# ============================================================

class LoginRequest(BaseModel):
    """
    Data required when a user logs in.
    """

    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=8
    )


# ============================================================
# 3. LOGIN RESPONSE
# ============================================================

class TokenResponse(BaseModel):
    """
    JWT token returned after successful login.
    """

    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ============================================================
# 4. CURRENT USER RESPONSE
# ============================================================

class CurrentUserResponse(BaseModel):
    """
    Information returned by /auth/me.
    """

    username: str
    email: str
    role: str