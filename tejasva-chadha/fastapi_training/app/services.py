from typing import List, Optional
from app.schemas import StudentCreate, StudentResponse, StudentUpdate


# Initial sample seed data
INITIAL_STUDENTS = [
    {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "age": 22,
        "marks": 88.5,
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Bob Johnson",
        "email": "bob.johnson@example.com",
        "age": 24,
        "marks": 75.0,
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "age": 20,
        "marks": 45.0,
        "is_active": False,
    },
    {
        "id": 4,
        "name": "Diana Prince",
        "email": "diana.prince@example.com",
        "age": 25,
        "marks": 92.0,
        "is_active": True,
    },
]


class StudentService:
    def __init__(self):
        self.reset_db()

    def reset_db(self) -> None:
        """Reset the in-memory database to default seed state."""
        self._students: List[dict] = [dict(s) for s in INITIAL_STUDENTS]
        self._next_id: int = 5

    def get_health_status(self) -> dict:
        """Return application health check status."""
        return {
            "status": "healthy",
            "service": "fastapi-student-api",
            "database": "in-memory",
            "total_students": len(self._students),
        }

    def list_students(
        self,
        skip: int = 0,
        limit: int = 10,
        is_active: Optional[bool] = None,
        min_marks: Optional[float] = None,
    ) -> List[StudentResponse]:
        """
        List students with filtering by active status and minimum marks,
        plus pagination using skip and limit.
        """
        filtered = self._students

        if is_active is not None:
            filtered = [s for s in filtered if s["is_active"] == is_active]

        if min_marks is not None:
            filtered = [s for s in filtered if s["marks"] >= min_marks]

        paginated = filtered[skip : skip + limit]
        return [StudentResponse(**s) for s in paginated]

    def get_student(self, student_id: int) -> Optional[StudentResponse]:
        """Retrieve a single student by unique ID."""
        for s in self._students:
            if s["id"] == student_id:
                return StudentResponse(**s)
        return None

    def create_student(self, student_data: StudentCreate) -> StudentResponse:
        """Create a new student record with auto-incremented ID."""
        new_student = student_data.model_dump()
        new_student["id"] = self._next_id
        self._next_id += 1
        self._students.append(new_student)
        return StudentResponse(**new_student)

    def update_student(
        self, student_id: int, student_data: StudentUpdate
    ) -> Optional[StudentResponse]:
        """Partially update an existing student record."""
        for s in self._students:
            if s["id"] == student_id:
                update_data = student_data.model_dump(exclude_unset=True)
                s.update(update_data)
                return StudentResponse(**s)
        return None

    def delete_student(self, student_id: int) -> bool:
        """Delete a student record by ID. Returns True if deleted, False if not found."""
        for i, s in enumerate(self._students):
            if s["id"] == student_id:
                self._students.pop(i)
                return True
        return False


# Global service singleton instance
student_service = StudentService()
