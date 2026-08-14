from fastapi import FastAPI, HTTPException, Query, status

from .schemas import StudentCreate, StudentResponse
from .services import (
    create_student,
    delete_student,
    get_all_students,
    get_student,
    update_student,
)


app = FastAPI(
    title="Student Training Portal API",
    description="Introductory FastAPI Student CRUD API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Student Training Portal API",
    }


@app.get(
    "/students",
    response_model=list[StudentResponse],
)
def list_students(
    active: bool | None = Query(default=None),
    min_marks: float | None = Query(
        default=None,
        ge=0,
        le=100,
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
):
    return get_all_students(
        active=active,
        min_marks=min_marks,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
)
def retrieve_student(student_id: int):

    student = get_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return student


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_student(student: StudentCreate):

    return create_student(student)


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
)
def patch_student(
    student_id: int,
    student: StudentCreate,
):

    updated_student = update_student(
        student_id,
        student,
    )

    if updated_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return updated_student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_student(student_id: int):

    deleted = delete_student(student_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return None