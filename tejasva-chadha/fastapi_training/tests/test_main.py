import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import student_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_student_database():
    """Reset the in-memory database before every test for test isolation."""
    student_service.reset_db()


def test_health_check():
    """Test 1: GET /health returns application status code 200 and healthy metadata."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "fastapi-student-api"
    assert "total_students" in data


def test_list_all_students():
    """Test 2: GET /students returns initial seed list of students."""
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4
    assert data[0]["name"] == "Alice Smith"


def test_get_student_by_id_success():
    """Test 3: GET /students/{id} retrieves existing student."""
    response = client.get("/students/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice Smith"
    assert data["email"] == "alice.smith@example.com"


def test_get_student_by_id_not_found():
    """Test 4: GET /students/{id} returns 404 for missing student ID."""
    response = client.get("/students/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student with ID 999 not found"


def test_create_student_success():
    """Test 5: POST /students creates a student record with valid payload (status 201)."""
    payload = {
        "name": "Eve Adams",
        "email": "eve.adams@example.com",
        "age": 21,
        "marks": 95.0,
        "is_active": True,
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 5
    assert data["name"] == "Eve Adams"
    assert data["email"] == "eve.adams@example.com"
    assert data["marks"] == 95.0


def test_create_student_validation_invalid_age():
    """Test 6: POST /students returns 422 if age is outside 16-60 range."""
    # Underage student (15)
    payload_young = {
        "name": "Young Student",
        "email": "young@example.com",
        "age": 15,
        "marks": 80.0,
    }
    response_young = client.post("/students", json=payload_young)
    assert response_young.status_code == 422

    # Overage student (61)
    payload_old = {
        "name": "Old Student",
        "email": "old@example.com",
        "age": 61,
        "marks": 80.0,
    }
    response_old = client.post("/students", json=payload_old)
    assert response_old.status_code == 422


def test_create_student_validation_invalid_marks():
    """Test 7: POST /students returns 422 if marks are not between 0 and 100."""
    # Marks < 0
    payload_neg = {
        "name": "Negative Marks",
        "email": "neg@example.com",
        "age": 20,
        "marks": -5.0,
    }
    response_neg = client.post("/students", json=payload_neg)
    assert response_neg.status_code == 422

    # Marks > 100
    payload_over = {
        "name": "Over Marks",
        "email": "over@example.com",
        "age": 20,
        "marks": 105.0,
    }
    response_over = client.post("/students", json=payload_over)
    assert response_over.status_code == 422


def test_create_student_validation_invalid_email():
    """Test 8: POST /students returns 422 for malformed email address."""
    payload = {
        "name": "Bad Email",
        "email": "not-an-email",
        "age": 22,
        "marks": 70.0,
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 422


def test_update_student_success():
    """Test 9: PATCH /students/{id} partially updates student attributes."""
    payload = {"marks": 99.0, "name": "Alice Smith Updated"}
    response = client.patch("/students/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice Smith Updated"
    assert data["marks"] == 99.0
    assert data["email"] == "alice.smith@example.com"  # unchanged field remains intact


def test_update_student_not_found():
    """Test 10: PATCH /students/{id} returns 404 for missing student ID."""
    payload = {"marks": 90.0}
    response = client.patch("/students/999", json=payload)
    assert response.status_code == 404


def test_delete_student_success():
    """Test 11: DELETE /students/{id} removes student record (204 No Content)."""
    response = client.delete("/students/1")
    assert response.status_code == 204

    # Verify student no longer exists
    get_res = client.get("/students/1")
    assert get_res.status_code == 404


def test_delete_student_not_found():
    """Test 12: DELETE /students/{id} returns 404 for missing student ID."""
    response = client.delete("/students/999")
    assert response.status_code == 404


def test_filter_students_by_is_active():
    """Test 13: GET /students filters records by active status."""
    res_active = client.get("/students?is_active=true")
    assert res_active.status_code == 200
    data_active = res_active.json()
    assert all(s["is_active"] is True for s in data_active)

    res_inactive = client.get("/students?is_active=false")
    assert res_inactive.status_code == 200
    data_inactive = res_inactive.json()
    assert len(data_inactive) == 1
    assert data_inactive[0]["name"] == "Charlie Brown"


def test_filter_students_by_min_marks():
    """Test 14: GET /students filters records by minimum marks."""
    response = client.get("/students?min_marks=80")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Alice (88.5) and Diana (92.0)
    assert all(s["marks"] >= 80.0 for s in data)


def test_pagination_students():
    """Test 15: GET /students handles pagination using skip and limit parameters."""
    response = client.get("/students?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 2
    assert data[1]["id"] == 3
