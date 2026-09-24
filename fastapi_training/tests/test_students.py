from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_get_student_by_id():
    response = client.get("/students/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Ruchi"

def test_get_student_not_found():
    response = client.get("/students/999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Student not found"

def test_create_student():
    new_student = {
        "name": "Neha",
        "email": "neha@example.com",
        "age": 21,
        "marks": 88,
        "active_status": True
    }

    response = client.post("/students", json=new_student)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Neha"
    assert data["marks"] == 88
    assert "id" in data

def test_create_student_invalid_email():
    new_student = {
        "name": "Neha",
        "email": "invalid-email",
        "age": 21,
        "marks": 88,
        "active_status": True
    }

    response = client.post("/students", json=new_student)

    assert response.status_code == 422

def test_create_student_invalid_age():
    new_student = {
        "name": "Neha",
        "email": "neha2@example.com",
        "age": 15,
        "marks": 88,
        "active_status": True
    }

    response = client.post("/students", json=new_student)

    assert response.status_code == 422

def test_create_student_invalid_marks():
    new_student = {
        "name": "Neha",
        "email": "neha3@example.com",
        "age": 21,
        "marks": 101,
        "active_status": True
    }

    response = client.post("/students", json=new_student)

    assert response.status_code == 422

def test_update_student():
    update_data = {
        "marks": 95
    }

    response = client.patch("/students/1", json=update_data)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["marks"] == 95

def test_delete_student():
    response = client.delete("/students/2")

    assert response.status_code == 204