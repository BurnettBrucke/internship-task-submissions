students = [
    {
        "id": 1,
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "age": 21,
        "marks": 85,
        "active": True
    },
    {
        "id": 2,
        "name": "Priya Verma",
        "email": "priya@example.com",
        "age": 22,
        "marks": 92,
        "active": True
    },
    {
        "id": 3,
        "name": "Aman Gupta",
        "email": "aman@example.com",
        "age": 20,
        "marks": 65,
        "active": False
    }
]

## Getting all students
def get_all_students():
    return students

#  Getting students by id
def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return None

#  Creating student
def create_student(student_data: dict):
    new_id = max([student["id"] for student in students], default=0) + 1

    new_student = {
        "id": new_id,
        **student_data
    }

    students.append(new_student)

    return new_student

#  updating students
def update_student(student_id: int, student_data: dict):
    student = get_student_by_id(student_id)

    if student is None:
        return None

    for key, value in student_data.items():
        if value is not None:
            student[key] = value

    return student


def delete_student(student_id: int):
    student = get_student_by_id(student_id)

    if student is None:
        return False

    students.remove(student)

    return True