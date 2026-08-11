"""FastAPI entry point.

Run locally with:
    uvicorn app.main:app --reload

Then open:
    http://127.0.0.1:8000/docs    (Swagger UI, generated automatically)
    http://127.0.0.1:8000/redoc   (ReDoc, generated automatically)

Both docs pages are built entirely from the type hints and Pydantic models
below (path/query params, request bodies, response_model) -- nothing here
manually maintains a docs page the way Django would need drf-spectacular or
similar bolted on.
"""
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status

from . import services
from .schemas import HealthResponse, PaginatedStudents, StudentCreate, StudentResponse, StudentUpdate

app = FastAPI(
    title="Student Training Portal API",
    description="A small FastAPI slice of the student system.",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health_check():
    """1. GET /health returning application status."""
    return {"status": "ok", "service": "student-training-portal-api"}


@app.get("/students", response_model=PaginatedStudents, tags=["students"])
def list_students(
    skip: int = Query(default=0, ge=0, description="Number of records to skip."),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return."),
    is_active: Optional[bool] = Query(default=None, description="Filter by active status."),
    min_marks: Optional[float] = Query(default=None, ge=0, le=100, description="Only students with marks >= this value."),
):
    """2. GET /students returning a list, with filtering and pagination.

    FastAPI challenge items covered here:
    - Filtering by active status and minimum marks (`is_active`, `min_marks`)
    - Pagination using `skip` and `limit` query parameters
    """
    results, total = services.list_students(skip=skip, limit=limit, is_active=is_active, min_marks=min_marks)
    return {"count": total, "skip": skip, "limit": limit, "results": results}


@app.get("/students/{student_id}", response_model=StudentResponse, tags=["students"])
def get_student(student_id: int):
    """3. GET /students/{student_id}. 7. Returns 404 when missing."""
    student = services.get_student(student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found.")
    return student


@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["students"])
def create_student(payload: StudentCreate):
    """4. POST /students using a Pydantic request model.

    Validation (age 16-60, marks 0-100, valid email) happens automatically
    via the StudentCreate/StudentBase field constraints in schemas.py --
    FastAPI returns a 422 with a detailed field-by-field error body before
    this function body even runs if the payload doesn't satisfy them.
    """
    return services.create_student(payload)


@app.patch("/students/{student_id}", response_model=StudentResponse, tags=["students"])
def update_student(student_id: int, payload: StudentUpdate):
    """5. PATCH /students/{student_id}. Partial update -- only fields
    present in the request body are changed."""
    student = services.update_student(student_id, payload)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found.")
    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["students"])
def delete_student(student_id: int):
    """6. DELETE /students/{student_id}."""
    deleted = services.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found.")
    return None
