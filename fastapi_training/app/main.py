from fastapi import FastAPI, HTTPException, status, Query

from app.schemas import StudentCreate, StudentUpdate, StudentResponse
from app import services

app = FastAPI(
    title="Student Training API",
    description="FastAPI project for Student Training Portal",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Student Training API is running"
    }


@app.get("/students", response_model=list[StudentResponse])
def get_students(
    active_status: bool | None = None,
    min_marks: float | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    return services.get_all_students(
        active_status=active_status,
        min_marks=min_marks,
        skip=skip,
        limit=limit
    )


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    student = services.get_student_by_id(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate):
    return services.create_student(student.model_dump())

@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(student_id: int, student: StudentUpdate):
    student_data = student.model_dump(exclude_unset=True)

    updated_student = services.update_student(
        student_id,
        student_data
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
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
            status_code=404,
            detail="Student not found"
        )

    return None