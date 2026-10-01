from fastapi import FastAPI, HTTPException , Query

from app import services
from app.schemas import StudentCreate, StudentResponse, StudentUpdate


app = FastAPI(
    title="Student Management API",
    description="A small FastAPI for the student system",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/students", response_model=list[StudentResponse])
def get_students(
    active: bool | None = None,
    min_marks: float | None = Query(default=None, ge=0, le=100),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    return services.get_students(
        active=active,
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


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate):
    return services.create_student(student)


@app.patch("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate):
    update_data = student.model_dump(exclude_unset=True)

    updated_student = services.update_student(
        student_id,
        update_data
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    deleted = services.delete_student(student_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )