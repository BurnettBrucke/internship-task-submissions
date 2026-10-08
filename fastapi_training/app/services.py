students = [
    {
        "id": 1,
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "age": 22,
        "marks": 85,
        "active": True
    },
    {
        "id": 2,
        "name": "Priya Singh",
        "email": "priya@example.com",
        "age": 21,
        "marks": 91,
        "active": True
    },
    {
        "id": 3,
        "name": "Amit Kumar",
        "email": "amit@example.com",
        "age": 23,
        "marks": 65,
        "active": False
    }
]


def get_students(
    active: bool | None = None,
    min_marks: float | None = None,
    skip: int = 0,
    limit: int = 10
):
    filtered_students = students

    if active is not None:
        filtered_students = [
            student
            for student in filtered_students
            if student["active"] == active
        ]

    if min_marks is not None:
        filtered_students = [
            student
            for student in filtered_students
            if student["marks"] >= min_marks
        ]

    return filtered_students[skip:skip + limit]


def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student

    return None


def create_student(student_data):
    new_id = max(student["id"] for student in students) + 1

    new_student = {
        "id": new_id,
        **student_data.model_dump()
    }

    students.append(new_student)

    return new_student


def update_student(student_id, student_data):
    student = get_student(student_id)

    if student is None:
        return None

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    student.update(update_data)

    return student


def delete_student(student_id):
    student = get_student(student_id)

    if student is None:
        return None

    students.remove(student)

    return student