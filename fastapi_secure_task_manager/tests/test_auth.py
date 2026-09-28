from fastapi.testclient import TestClient

from app.main import app
from app.data.store import users, tasks


client = TestClient(app)


def setup_function():
    users.clear()
    tasks.clear()


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass@123",
            "role": "user"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_username():
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass@123",
        "role": "user"
    }

    client.post(
        "/api/v1/auth/register",
        json=payload
    )

    response = client.post(
        "/api/v1/auth/register",
        json=payload
    )

    assert response.status_code == 409

    data = response.json()

    assert data["error"]["code"] == "USERNAME_ALREADY_EXISTS"


def test_valid_login():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass@123",
            "role": "user"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "StrongPass@123"
        }
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
            "email": "test@example.com",
            "password": "StrongPass@123",
            "role": "user"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["error"]["code"] == "INVALID_CREDENTIALS"


def test_me_without_token():
    response = client.get(
        "/api/v1/auth/me"
    )

    assert response.status_code == 401

    data = response.json()

    assert data["error"]["code"] == "AUTHENTICATION_REQUIRED"

def test_invalid_email():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "emailuser",
            "email": "invalid-email",
            "password": "StrongPass@123",
            "role": "user"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_weak_password():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "weakuser",
            "email": "weak@example.com",
            "password": "123",
            "role": "user"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_me_with_valid_token():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "meuser",
            "email": "me@example.com",
            "password": "StrongPass@123",
            "role": "user"
        }
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "meuser",
            "password": "StrongPass@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "meuser"
    assert data["email"] == "me@example.com"





