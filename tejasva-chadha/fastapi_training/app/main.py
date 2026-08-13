from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status

from app.schemas import StudentCreate, StudentResponse, StudentUpdate
from app.services import student_service

app = FastAPI(
    title="Student Training API",
    description="FastAPI application for managing student training records with validation, filtering, and pagination.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    tags=["Health"],
)
def get_health():
    """
    Check application health status and service metadata.
    """
    return student_service.get_health_status()


@app.get(
    "/students",
    response_model=List[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="List all students with filtering and pagination",
    tags=["Students"],
)
def list_students(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status (true/false)"),
    min_marks: Optional[float] = Query(None, ge=0.0, le=100.0, description="Filter by minimum marks (0-100)"),
):
    """
    Retrieve list of students. Supports query parameters for filtering and pagination:
    - **skip**: Number of records to offset (default 0)
    - **limit**: Maximum records per page (default 10, max 100)
    - **is_active**: Filter active or inactive students
    - **min_marks**: Filter students with marks >= min_marks
    """
    return student_service.list_students(
        skip=skip, limit=limit, is_active=is_active, min_marks=min_marks
    )


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single student by ID",
    tags=["Students"],
)
def get_student(student_id: int):
    """
    Retrieve details of a specific student by ID.
    Returns **404 Not Found** if the student does not exist.
    """
    student = student_service.get_student(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return student


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student record",
    tags=["Students"],
)
def create_student(student_data: StudentCreate):
    """
    Create a new student record with validation:
    - **name**: 2-100 characters
    - **email**: valid email address
    - **age**: 16 to 60 years
    - **marks**: 0.0 to 100.0
    """
    return student_service.create_student(student_data)


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Partially update a student record",
    tags=["Students"],
)
def update_student(student_id: int, student_data: StudentUpdate):
    """
    Update selected fields of an existing student by ID.
    Returns **404 Not Found** if student is not found.
    """
    updated = student_service.update_student(student_id, student_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return updated


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student record",
    tags=["Students"],
)
def delete_student(student_id: int):
    """
    Delete a student record by ID.
    Returns **204 No Content** on success, or **404 Not Found** if student does not exist.
    """
    deleted = student_service.delete_student(student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return None
