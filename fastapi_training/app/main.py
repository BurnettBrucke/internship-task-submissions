from fastapi import FastAPI, HTTPException, Query, status
from typing import Optional

from .schemas import StudentCreate, StudentUpdate, StudentResponse
from . import services


app = FastAPI(
    title="Student Training API",
    version="1.0.0",
    description="Simple FastAPI project for Task 3"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Student Training API is running"
    }


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    active: Optional[bool] = None,
    min_marks: Optional[float] = Query(
        None,
        ge=0,
        le=100
    )
):
    return services.get_all_students(
        skip=skip,
        limit=limit,
        active=active,
        min_marks=min_marks
    )


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: int):

    student = services.get_student_by_id(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate):

    return services.create_student(
        student.model_dump()
    )


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentUpdate
):

    updated_student = services.update_student(
        student_id,
        student.model_dump(exclude_unset=True)
    )

    if updated_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return updated_student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(student_id: int):

    deleted = services.delete_student(student_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return None