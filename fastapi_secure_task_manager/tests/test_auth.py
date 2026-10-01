from fastapi.testclient import TestClient

from app.main import app
from app.data.store import users_db, tasks_db


client = TestClient(app)


def setup_function():
    users_db.clear()
    tasks_db.clear()

    import app.data.store as store
    store.next_task_id = 1


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestUser@123",
            "role": "user",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "user"

    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_username():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestUser@123",
            "role": "user",
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "Another@123",
            "role": "user",
        },
    )

    assert response.status_code == 409

def test_duplicate_email(client):
    payload = {
        "username": "user_one",
        "email": "duplicate@example.com",
        "password": "TestUser@123",
        "role": "user",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201

    duplicate_email_payload = {
        "username": "user_two",
        "email": "duplicate@example.com",
        "password": "TestUser@123",
        "role": "user",
    }

    response = client.post(
        "/api/v1/auth/register",
        json=duplicate_email_payload,
    )

    assert response.status_code == 409


def test_invalid_email():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "TestUser@123",
            "role": "user",
        },
    )

    assert response.status_code == 422


def test_short_password():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "123",
            "role": "user",
        },
    )

    assert response.status_code == 422


def test_login_success():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestUser@123",
            "role": "user",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "TestUser@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800


def test_invalid_login():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestUser@123",
            "role": "user",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "WrongPassword@123",
        },
    )

    assert response.status_code == 401


def test_me_requires_authentication():
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_with_valid_token():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestUser@123",
            "role": "user",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "TestUser@123",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "user"

def test_login_blocked_after_five_failed_attempts():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "lockuser",
            "email": "lockuser@example.com",
            "password": "CorrectPass@123",
            "role": "user",
        },
    )

    # Five failed login attempts
    for _ in range(5):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "lockuser",
                "password": "WrongPass@123",
            },
        )

        assert response.status_code == 401

    # Sixth attempt should also be blocked
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "lockuser",
            "password": "CorrectPass@123",
        },
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
    assert "Too many failed login attempts" in response.json()["error"]["message"]


def test_successful_login_resets_failed_attempts():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "resetuser",
            "email": "resetuser@example.com",
            "password": "CorrectPass@123",
            "role": "user",
        },
    )

    # Two failed attempts
    for _ in range(2):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "resetuser",
                "password": "WrongPass@123",
            },
        )

        assert response.status_code == 401

    # Correct password should reset the counter
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "resetuser",
            "password": "CorrectPass@123",
        },
    )

    assert response.status_code == 200

    # Another failed attempt should start from 1 again,
    # not continue from 3.
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "resetuser",
            "password": "WrongPass@123",
        },
    )

    assert response.status_code == 401

# ============================================================
# INVALID JWT TOKEN
# ============================================================

def test_invalid_jwt_token_returns_401():
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid.jwt.token"
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["error"]["code"] == "UNAUTHORIZED"
    assert data["error"]["message"] == "Invalid or expired token"