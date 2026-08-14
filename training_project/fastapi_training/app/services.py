from .schemas import StudentCreate, StudentResponse


students = [
    StudentResponse(
        id=1,
        name="Aarav Sharma",
        email="aarav@example.com",
        age=21,
        marks=85,
        active=True,
    ),
    StudentResponse(
        id=2,
        name="Priya Verma",
        email="priya@example.com",
        age=22,
        marks=78,
        active=True,
    ),
    StudentResponse(
        id=3,
        name="Rahul Mehta",
        email="rahul@example.com",
        age=20,
        marks=92,
        active=False,
    ),
]


def get_all_students(
    active: bool | None = None,
    min_marks: float | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[StudentResponse]:

    result = students.copy()

    if active is not None:
        result = [
            student
            for student in result
            if student.active == active
        ]

    if min_marks is not None:
        result = [
            student
            for student in result
            if student.marks >= min_marks
        ]

    return result[skip:skip + limit]


def get_student(student_id: int) -> StudentResponse | None:

    for student in students:
        if student.id == student_id:
            return student

    return None


def create_student(
    student_data: StudentCreate,
) -> StudentResponse:

    next_id = max(
        (student.id for student in students),
        default=0,
    ) + 1

    student = StudentResponse(
        id=next_id,
        **student_data.model_dump(),
    )

    students.append(student)

    return student


def update_student(
    student_id: int,
    student_data: StudentCreate,
) -> StudentResponse | None:

    student = get_student(student_id)

    if student is None:
        return None

    updated_student = StudentResponse(
        id=student_id,
        **student_data.model_dump(),
    )

    index = students.index(student)
    students[index] = updated_student

    return updated_student


def delete_student(student_id: int) -> bool:

    student = get_student(student_id)

    if student is None:
        return False

    students.remove(student)

    return True