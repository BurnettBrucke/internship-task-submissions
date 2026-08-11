"""Pydantic models (schemas) for the FastAPI student API.

Kept separate from main.py (which only wires up routes) and services.py
(which only handles data operations) so each file has one job -- exactly
the same "don't mix concerns" reasoning behind the Django project's
services.py split.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=16, le=60, description="Age must be between 16 and 60.")
    marks: float = Field(ge=0, le=100, description="Marks must be between 0 and 100.")
    is_active: bool = True


class StudentCreate(StudentBase):
    """Request body for POST /students."""
    pass


class StudentUpdate(BaseModel):
    """Request body for PATCH /students/{student_id} -- every field optional
    since a PATCH only sends the fields being changed."""
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=16, le=60)
    marks: Optional[float] = Field(default=None, ge=0, le=100)
    is_active: Optional[bool] = None


class StudentResponse(StudentBase):
    """Response body -- includes the server-assigned id."""
    model_config = ConfigDict(from_attributes=True)

    id: int


class HealthResponse(BaseModel):
    status: str
    service: str


class PaginatedStudents(BaseModel):
    """Response shape for GET /students, mirroring the pagination shape
    used elsewhere in the project (count/results) so a client switching
    between this API and a future DRF-based Django API sees a familiar
    contract."""
    count: int
    skip: int
    limit: int
    results: list[StudentResponse]
