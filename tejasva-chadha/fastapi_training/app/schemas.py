from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Name of the student (2-100 characters)")
    email: EmailStr = Field(..., description="Valid email address of the student")
    age: int = Field(..., ge=16, le=60, description="Age of student (must be between 16 and 60)")
    marks: float = Field(..., ge=0.0, le=100.0, description="Marks of student (must be between 0 and 100)")
    is_active: bool = Field(default=True, description="Active status of student")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Updated name of student")
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    age: Optional[int] = Field(None, ge=16, le=60, description="Updated age (16-60)")
    marks: Optional[float] = Field(None, ge=0.0, le=100.0, description="Updated marks (0-100)")
    is_active: Optional[bool] = Field(None, description="Updated active status")


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique integer ID of student")

