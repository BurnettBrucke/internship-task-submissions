students = [
    {
        "id": 1,
        "name": "Jaya",
        "email": "jaya@test.com",
        "age": 22,
        "course": "B.Tech",
        "marks": 85,
        "active": True
    },
    {
        "id": 2,
        "name": "Rahul",
        "email": "rahul@test.com",
        "age": 21,
        "course": "BCA",
        "marks": 78,
        "active": True
    },
    {
        "id": 3,
        "name": "Priya",
        "email": "priya@test.com",
        "age": 23,
        "course": "B.Tech",
        "marks": 92,
        "active": False
    }
]


def get_all_students(
    skip=0,
    limit=10,
    active=None,
    min_marks=None
):
    result = students.copy()

    if active is not None:
        result = [
            student
            for student in result
            if student["active"] == active
        ]

    if min_marks is not None:
        result = [
            student
            for student in result
            if student["marks"] >= min_marks
        ]

    return result[skip:skip + limit]


def get_student_by_id(student_id):
    for student in students:
        if student["id"] == student_id:
            return student

    return None


def create_student(student_data):
    new_id = max([student["id"] for student in students], default=0) + 1

    new_student = {
        "id": new_id,
        **student_data
    }

    students.append(new_student)

    return new_student


def update_student(student_id, student_data):
    student = get_student_by_id(student_id)

    if student is None:
        return None

    for key, value in student_data.items():
        if value is not None:
            student[key] = value

    return student


def delete_student(student_id):
    student = get_student_by_id(student_id)

    if student is None:
        return False

    students.remove(student)

    return True