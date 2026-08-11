from fastapi import FastAPI, HTTPException, Query, status

from app.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from app.services import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)


app = FastAPI(
    title="Student Training API",
    description="A simple FastAPI Student Management API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Student Training API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Student API is running"
    }


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    active: bool | None = None,
    min_marks: float | None = Query(default=None, ge=0, le=100),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    students = get_all_students()

    if active is not None:
        students = [
            student for student in students
            if student["active"] == active
        ]

    if min_marks is not None:
        students = [
            student for student in students
            if student["marks"] >= min_marks
        ]

    return students[skip:skip + limit]


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: int):
    student = get_student_by_id(student_id)

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
def create_new_student(student: StudentCreate):
    return create_student(student.model_dump())


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_existing_student(
    student_id: int,
    student: StudentUpdate
):
    updated_student = update_student(
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
def delete_existing_student(student_id: int):
    deleted = delete_student(student_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return None