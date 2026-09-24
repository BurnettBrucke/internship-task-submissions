from fastapi.testclient import TestClient

from app.main import app
from app import services


client = TestClient(app)


def reset_students():
    services.students.clear()

    services.students.extend([
        {
            "id": 1,
            "name": "Ramya Rathod",
            "email": "ramya@example.com",
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
    ])
# 1. Health endpoint
def test_health():
    reset_students()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# 2. Get all students
def test_get_students():
    reset_students()

    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 3


# 3. Get existing student
def test_get_student():
    reset_students()

    response = client.get("/students/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Ramya Rathod"


# 4. Get nonexistent student
def test_get_nonexistent_student():
    reset_students()

    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


# 5. Create valid student
def test_create_student():
    reset_students()

    student = {
        "name": "Neha Singh",
        "email": "neha@example.com",
        "age": 23,
        "marks": 88,
        "active": True,
    }

    response = client.post("/students", json=student)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Neha Singh"
    assert data["marks"] == 88
    assert data["active"] is True


# 6. Create student with invalid age
def test_create_student_invalid_age():
    reset_students()

    student = {
        "name": "Test Student",
        "email": "test@example.com",
        "age": 10,
        "marks": 80,
        "active": True,
    }

    response = client.post("/students", json=student)

    assert response.status_code == 422


# 7. Create student with invalid marks
def test_create_student_invalid_marks():
    reset_students()

    student = {
        "name": "Test Student",
        "email": "test@example.com",
        "age": 20,
        "marks": 150,
        "active": True,
    }

    response = client.post("/students", json=student)

    assert response.status_code == 422


# 8. Update student
def test_update_student():
    reset_students()

    response = client.patch(
        "/students/1",
        json={"marks": 95}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["marks"] == 95
    assert data["name"] == "Ramya Rathod"


# 9. Delete student
def test_delete_student():
    reset_students()

    response = client.delete("/students/2")

    assert response.status_code == 204

    response = client.get("/students/2")

    assert response.status_code == 404


# 10. Delete nonexistent student
def test_delete_nonexistent_student():
    reset_students()

    response = client.delete("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


# 11. Filter active students
def test_filter_active_students():
    reset_students()

    response = client.get("/students?active=true")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(student["active"] is True for student in data)


# 12. Filter by minimum marks
def test_filter_minimum_marks():
    reset_students()

    response = client.get("/students?min_marks=80")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Priya Verma"


# 13. Test pagination
def test_pagination():
    reset_students()

    response = client.get(
        "/students?skip=0&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Ramya Rathod"
    assert data[1]["name"] == "Priya Verma"


# 14. Invalid pagination
def test_invalid_pagination():
    reset_students()

    response = client.get(
        "/students?skip=-1"
    )

    assert response.status_code == 422
