# ============================================================
# 1. IMPORTS
# ============================================================

from enum import Enum

from pydantic import BaseModel, EmailStr, Field


# ============================================================
# 2. USER ROLE ENUM
# ============================================================

class UserRole(str, Enum):
    """
    Available roles in the application.
    """

    USER = "user"
    ADMIN = "admin"


# ============================================================
# 3. USER REGISTRATION SCHEMA
# ============================================================

class UserCreate(BaseModel):
    """
    Data required when registering a user.
    """

    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )

    role: UserRole = UserRole.USER


# ============================================================
# 4. USER RESPONSE SCHEMA
# ============================================================

class UserResponse(BaseModel):
    """
    Safe user data returned by the API.

    Password is intentionally excluded.
    """

    username: str
    email: EmailStr
    role: UserRole