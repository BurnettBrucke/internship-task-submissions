from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=16, le=60)
    course: str = Field(min_length=2, max_length=100)
    marks: float = Field(ge=0, le=100)
    active: bool = True


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=16, le=60)
    course: Optional[str] = Field(default=None, min_length=2, max_length=100)
    marks: Optional[float] = Field(default=None, ge=0, le=100)
    active: Optional[bool] = None


class StudentResponse(StudentCreate):
    id: int