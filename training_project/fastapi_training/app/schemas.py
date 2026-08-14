from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        ge=16,
        le=60
    )

    marks: float = Field(
        ge=0,
        le=100
    )

    active: bool = True


class StudentResponse(StudentCreate):
    id: int