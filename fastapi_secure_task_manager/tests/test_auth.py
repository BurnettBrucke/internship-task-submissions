from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "role": "user",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "user"


def test_duplicate_username():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicateuser",
            "email": "duplicate1@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicateuser",
            "email": "duplicate2@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409


def test_invalid_email():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "emailtest",
            "email": "invalid-email",
            "password": "password123",
        },
    )

    assert response.status_code == 422


def test_weak_password():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "weakpass",
            "email": "weakpass@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422


def test_login_returns_token():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "loginuser",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800


def test_wrong_password():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "wrongpass",
            "email": "wrongpass@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "wrongpass",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_auth_me():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "meuser",
            "email": "meuser@example.com",
            "password": "password123",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "meuser",
            "password": "password123",
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
    assert response.json()["username"] == "meuser"
    assert response.json()["role"] == "user"


def test_protected_endpoint_without_token():
    response = client.get("/api/v1/tasks")

    assert response.status_code == 401