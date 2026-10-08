from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def register_user(
    username,
    email,
    password="StrongPass@123",
    role="user",
):
    return client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        },
    )


def login_user(
    username,
    password="StrongPass@123",
):
    return client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )


def test_register_user():
    response = register_user(
        "testuser",
        "test@example.com",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_username():
    payload = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "StrongPass@123",
        "role": "user",
    }

    first_response = register_user(
        payload["username"],
        payload["email"],
        payload["password"],
        payload["role"],
    )

    assert first_response.status_code == 201

    response = register_user(
        payload["username"],
        "different@example.com",
        payload["password"],
        payload["role"],
    )

    assert response.status_code == 409

    data = response.json()

    assert data["error"]["code"] == "USERNAME_ALREADY_EXISTS"


def test_valid_login():
    register_response = register_user(
        "loginuser",
        "login@example.com",
    )

    assert register_response.status_code == 201

    response = login_user(
        "loginuser",
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800


def test_invalid_login():
    register_response = register_user(
        "invalidlogin",
        "invalidlogin@example.com",
    )

    assert register_response.status_code == 201

    response = login_user(
        "invalidlogin",
        "WrongPassword",
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
    response = register_user(
        "emailuser",
        "invalid-email",
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_weak_password():
    response = register_user(
        "weakuser",
        "weak@example.com",
        password="123",
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_me_with_valid_token():
    register_response = register_user(
        "meuser",
        "me@example.com",
    )

    assert register_response.status_code == 201

    login_response = login_user(
        "meuser",
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "meuser"
    assert data["email"] == "me@example.com"