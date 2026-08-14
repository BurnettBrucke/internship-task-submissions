from fastapi.testclient import TestClient

from fastapi_training.app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student():
    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_student_not_found():
    response = client.get("/students/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_create_student():
    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "email": "test.student@example.com",
            "age": 22,
            "marks": 85,
            "active": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Student"
    assert data["marks"] == 85


def test_invalid_email():
    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "email": "invalid-email",
            "age": 22,
            "marks": 85,
            "active": True,
        },
    )

    assert response.status_code == 422


def test_invalid_age():
    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "email": "age.test@example.com",
            "age": 15,
            "marks": 85,
            "active": True,
        },
    )

    assert response.status_code == 422


def test_invalid_marks():
    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "email": "marks.test@example.com",
            "age": 22,
            "marks": 101,
            "active": True,
        },
    )

    assert response.status_code == 422


def test_update_student():
    response = client.patch(
        "/students/1",
        json={
            "name": "Updated Student",
            "email": "updated.student@example.com",
            "age": 23,
            "marks": 95,
            "active": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Student"
    assert response.json()["marks"] == 95


def test_delete_student():
    # Create a student specifically for deletion.
    create_response = client.post(
        "/students",
        json={
            "name": "Delete Student",
            "email": "delete.student@example.com",
            "age": 21,
            "marks": 70,
            "active": True,
        },
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/students/{student_id}"
    )

    assert delete_response.status_code == 204


def test_delete_missing_student():
    response = client.delete("/students/9999")

    assert response.status_code == 404


def test_active_filter():
    response = client.get("/students?active=true")

    assert response.status_code == 200

    students = response.json()

    assert all(student["active"] is True for student in students)


def test_minimum_marks_filter():
    response = client.get("/students?min_marks=80")

    assert response.status_code == 200

    students = response.json()

    assert all(student["marks"] >= 80 for student in students)


def test_pagination():
    response = client.get("/students?skip=0&limit=2")

    assert response.status_code == 200

    students = response.json()

    assert len(students) <= 2