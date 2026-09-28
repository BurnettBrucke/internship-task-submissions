from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100
    )

    role: Literal["user", "admin"] = "user"


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Literal["user", "admin"]