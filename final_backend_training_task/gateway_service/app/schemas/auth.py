from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=100,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class RegisterResponse(BaseModel):
    id: int
    username: str
    created_at: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
