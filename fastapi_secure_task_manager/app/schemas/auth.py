from typing import Literal

from pydantic import BaseModel , EmailStr , Field

class RegisterRequest(BaseModel):
    username : str = Field(min_length=3 , max_length=50)
    email : EmailStr
    password : str = Field(min_length=8 , max_length=128)
    role : Literal["user", "admin"] = "user"

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int