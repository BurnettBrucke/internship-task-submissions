from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["user", "admin"] = "user"


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    role: Literal["user", "admin"]