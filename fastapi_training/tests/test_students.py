import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import services


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_students():
    services.students.clear()

    services.students.extend([
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
    ])


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_single_student():
    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Rahul Sharma"


def test_student_not_found():
    response = client.get("/students/999")

    assert response.status_code == 404


def test_create_student():
    response = client.post(
        "/students",
        json={
            "name": "Amit Verma",
            "email": "amitverma@example.com",
            "age": 24,
            "marks": 88
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Amit Verma"


def test_invalid_email():
    response = client.post(
        "/students",
        json={
            "name": "Amit Verma",
            "email": "invalid-email",
            "age": 24,
            "marks": 88
        }
    )

    assert response.status_code == 422


def test_invalid_age():
    response = client.post(
        "/students",
        json={
            "name": "Amit Verma",
            "email": "amitverma@example.com",
            "age": 15,
            "marks": 88
        }
    )

    assert response.status_code == 422


def test_invalid_marks():
    response = client.post(
        "/students",
        json={
            "name": "Amit Verma",
            "email": "amitverma@example.com",
            "age": 24,
            "marks": 101
        }
    )

    assert response.status_code == 422


def test_patch_marks_only():
    response = client.patch(
        "/students/1",
        json={
            "marks": 95
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["marks"] == 95
    assert data["name"] == "Rahul Sharma"
    assert data["age"] == 22


def test_filter_active_students():
    response = client.get(
        "/students?active=true"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    for student in data:
        assert student["active"] is True


def test_filter_minimum_marks():
    response = client.get(
        "/students?min_marks=90"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["marks"] >= 90


def test_pagination():
    response = client.get(
        "/students?skip=1&limit=1"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 2


def test_delete_student():
    response = client.delete("/students/3")

    assert response.status_code == 204


def test_delete_missing_student():
    response = client.delete("/students/999")

    assert response.status_code == 404