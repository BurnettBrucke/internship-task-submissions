import uuid

import pytest


def unique_user(prefix):
    value = uuid.uuid4().hex[:8]
    return f"{prefix}_{value}", f"{prefix}_{value}@example.com"


@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(client):
    username, email = unique_user("register")

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
            "role": "user",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == username


@pytest.mark.asyncio(loop_scope="session")
async def test_duplicate_username(client):
    username, email = unique_user("duplicate")

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": f"second_{email}",
            "password": "password123",
        },
    )

    assert response.status_code == 409


@pytest.mark.asyncio(loop_scope="session")
async def test_invalid_email(client):
    username, _ = unique_user("invalid_email")

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": "invalid-email",
            "password": "password123",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_weak_password(client):
    username, email = unique_user("weak_password")

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "123",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_login_returns_token(client):
    username, email = unique_user("login")

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800


@pytest.mark.asyncio(loop_scope="session")
async def test_wrong_password(client):
    username, email = unique_user("wrong_password")

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_auth_me(client):
    username, email = unique_user("auth_me")

    await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == username
    assert response.json()["role"] == "user"


@pytest.mark.asyncio(loop_scope="session")
async def test_protected_endpoint_without_token(client):
    response = await client.get("/api/v1/tasks")

    assert response.status_code == 401