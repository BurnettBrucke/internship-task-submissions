from fastapi import FastAPI, Query, status

from .schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
)

from .services import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student,
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Student Management API",
    description="FastAPI Training Project - Student Management System",
    version="1.0.0",
)


# ============================================================
# 1. HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Student API is running"
    }


# ============================================================
# 2. GET ALL STUDENTS
# ============================================================

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    active: bool | None = None,
    min_marks: float | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    return get_all_students(
        active=active,
        min_marks=min_marks,
        skip=skip,
        limit=limit,
    )


# ============================================================
# 3. GET STUDENT BY ID
# ============================================================

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: int):
    return get_student_by_id(student_id)


# ============================================================
# 4. CREATE STUDENT
# ============================================================

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_student(student: StudentCreate):
    return create_student(student)


# ============================================================
# 5. UPDATE STUDENT
# ============================================================

@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student_data(
    student_id: int,
    student: StudentUpdate,
):
    return update_student(student_id, student)


# ============================================================
# 6. DELETE STUDENT
# ============================================================

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_student(student_id: int):
    delete_student(student_id)