students = [
    {
        "id": 1,
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "age": 21,
        "marks": 78,
        "active": True,
    },
    {
        "id": 2,
        "name": "Priya Verma",
        "email": "priya@example.com",
        "age": 22,
        "marks": 91,
        "active": True,
    },
    {
        "id": 3,
        "name": "Aman Patel",
        "email": "aman@example.com",
        "age": 20,
        "marks": 65,
        "active": False,
    },
]


def get_students(
    active=None,
    min_marks=None,
    skip=0,
    limit=10
):
    filtered_students = students

    # Active status filter
    if active is not None:
        filtered_students = [
            student
            for student in filtered_students
            if student["active"] == active
        ]

    # Minimum marks filter
    if min_marks is not None:
        filtered_students = [
            student
            for student in filtered_students
            if student["marks"] >= min_marks
        ]

    # Pagination
    return filtered_students[skip:skip + limit]


def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return None


def create_student(student_data):
    new_student = {
        "id": max(
            [student["id"] for student in students],
            default=0
        ) + 1,
        "name": student_data.name,
        "email": student_data.email,
        "age": student_data.age,
        "marks": student_data.marks,
        "active": student_data.active,
    }

    students.append(new_student)

    return new_student


def update_student(student_id: int, update_data):
    student = get_student_by_id(student_id)

    if student is None:
        return None

    student.update(update_data)

    return student


def delete_student(student_id: int):
    student = get_student_by_id(student_id)

    if student is None:
        return False

    students.remove(student)

    return True