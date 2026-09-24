students = [
    {
        "id": 1,
        "name": "Ruchi",
        "email": "ruchi@example.com",
        "age": 22,
        "marks": 85,
        "active_status": True,
    },
    {
        "id": 2,
        "name": "Aman",
        "email": "aman@example.com",
        "age": 24,
        "marks": 72,
        "active_status": True,
    },
]


def get_all_students(
    active_status=None,
    min_marks=None,
    skip=0,
    limit=10
):
    filtered_students = students

    if active_status is not None:
        filtered_students = [
            student
            for student in filtered_students
            if student["active_status"] == active_status
        ]

    if min_marks is not None:
        filtered_students = [
            student
            for student in filtered_students
            if student["marks"] >= min_marks
        ]

    return filtered_students[skip:skip + limit]


def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return None


def create_student(student_data):
    new_id = max(student["id"] for student in students) + 1

    new_student = {
        "id": new_id,
        **student_data,
    }

    students.append(new_student)

    return new_student

def update_student(student_id: int, student_data: dict):
    student = get_student_by_id(student_id)

    if student is None:
        return None

    student.update(student_data)

    return student

def delete_student(student_id: int):
    student = get_student_by_id(student_id)

    if student is None:
        return False

    students.remove(student)

    return True