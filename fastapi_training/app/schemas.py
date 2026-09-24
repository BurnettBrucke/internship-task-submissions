from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=16, le=60)
    marks: float = Field(ge=0, le=100)
    active_status: bool = True


class StudentResponse(StudentCreate):
    id: int

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=16, le=60)
    marks: float | None = Field(default=None, ge=0, le=100)
    active_status: bool | None = None