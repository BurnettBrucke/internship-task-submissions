"""FastAPI test suite.

Run with:
    pytest

Each test resets the in-memory store first (see the `client` fixture) so
tests don't leak state into each other -- the in-memory dict in
app/services.py is process-global, so without a reset, test order would
matter (a real anti-pattern to avoid, even in a toy in-memory store).
"""
import pytest
from fastapi.testclient import TestClient

from app import services
from app.main import app


@pytest.fixture
def client():
    services.seed_initial_data()  # 3 known students: ids 1, 2, 3
    return TestClient(app)


# ---------------------------------------------------------------------------
# 1. Health
# ---------------------------------------------------------------------------

def test_health_check_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "service" in body


# ---------------------------------------------------------------------------
# 2-3. List and retrieve
# ---------------------------------------------------------------------------

def test_list_students_returns_seeded_data(client):
    response = client.get("/students")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 3
    assert len(body["results"]) == 3


def test_get_single_student_returns_correct_record(client):
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Asha Verma"


def test_get_missing_student_returns_404(client):
    """7 / 19. Missing student IDs return 404."""
    response = client.get("/students/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# 4. Create
# ---------------------------------------------------------------------------

def test_create_student_success(client):
    payload = {"name": "New Student", "email": "new.student@example.com", "age": 22, "marks": 65}
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "New Student"
    assert body["id"] == 4  # after the 3 seeded students


def test_create_student_appears_in_subsequent_list(client):
    client.post("/students", json={"name": "New Student", "email": "extra@example.com", "age": 20, "marks": 50})
    response = client.get("/students")
    assert response.json()["count"] == 4


# ---------------------------------------------------------------------------
# 8 / 18. Validation: marks 0-100, age 16-60, valid email
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("field,bad_value", [
    ("age", 5),        # below 16
    ("age", 99),       # above 60
    ("marks", -1),      # below 0
    ("marks", 150),     # above 100
])
def test_create_student_rejects_out_of_range_values(client, field, bad_value):
    payload = {"name": "Bad Student", "email": "bad@example.com", "age": 20, "marks": 50}
    payload[field] = bad_value
    response = client.post("/students", json=payload)
    assert response.status_code == 422


def test_create_student_rejects_invalid_email(client):
    payload = {"name": "Bad Email", "email": "not-an-email", "age": 20, "marks": 50}
    response = client.post("/students", json=payload)
    assert response.status_code == 422


def test_create_student_rejects_missing_required_field(client):
    payload = {"email": "missing.name@example.com", "age": 20, "marks": 50}
    response = client.post("/students", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# 5. Update (PATCH)
# ---------------------------------------------------------------------------

def test_patch_updates_only_provided_fields(client):
    response = client.patch("/students/1", json={"marks": 99})
    assert response.status_code == 200
    body = response.json()
    assert body["marks"] == 99
    assert body["name"] == "Asha Verma"  # untouched


def test_patch_validates_updated_fields(client):
    response = client.patch("/students/1", json={"marks": 500})
    assert response.status_code == 422


def test_patch_missing_student_returns_404(client):
    response = client.patch("/students/999", json={"marks": 50})
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 6. Delete
# ---------------------------------------------------------------------------

def test_delete_student_success(client):
    response = client.delete("/students/1")
    assert response.status_code == 204
    assert client.get("/students/1").status_code == 404


def test_delete_missing_student_returns_404(client):
    response = client.delete("/students/999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def test_filter_by_active_status(client):
    response = client.get("/students", params={"is_active": False})
    body = response.json()
    assert body["count"] == 1
    assert all(s["is_active"] is False for s in body["results"])


def test_filter_by_minimum_marks(client):
    response = client.get("/students", params={"min_marks": 70})
    body = response.json()
    assert body["count"] == 2  # Asha (75) and Zara (91)
    assert all(s["marks"] >= 70 for s in body["results"])


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

def test_pagination_limit(client):
    response = client.get("/students", params={"limit": 2})
    body = response.json()
    assert body["count"] == 3       # total unaffected by pagination
    assert len(body["results"]) == 2  # but only 2 returned


def test_pagination_skip(client):
    first_page = client.get("/students", params={"limit": 1, "skip": 0}).json()
    second_page = client.get("/students", params={"limit": 1, "skip": 1}).json()
    assert first_page["results"][0]["id"] != second_page["results"][0]["id"]


# ---------------------------------------------------------------------------
# Docs
# ---------------------------------------------------------------------------

def test_swagger_docs_available(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_available(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()
