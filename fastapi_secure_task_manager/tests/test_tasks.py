import uuid

import pytest


def unique_user(prefix):
    value = uuid.uuid4().hex[:8]
    return f"{prefix}_{value}", f"{prefix}_{value}@example.com"


async def get_token(
    client,
    username,
    email,
    password="password123",
    role="user",
):
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        },
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


@pytest.mark.asyncio(loop_scope="session")
async def test_create_task(client):
    username, email = unique_user("create")

    token = await get_token(
        client,
        username,
        email,
    )

    response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Learn FastAPI",
            "description": "Complete security task",
            "priority": "high",
            "completed": False,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Learn FastAPI"
    assert response.json()["priority"] == "high"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks(client):
    username, email = unique_user("get")

    token = await get_token(
        client,
        username,
        email,
    )

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test task",
            "priority": "medium",
        },
    )

    assert create_response.status_code == 201

    response = await client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio(loop_scope="session")
async def test_update_task(client):
    username, email = unique_user("update")

    token = await get_token(
        client,
        username,
        email,
    )

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Old title",
            "priority": "low",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated title",
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["completed"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_task(client):
    username, email = unique_user("delete")

    token = await get_token(
        client,
        username,
        email,
    )

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Delete me",
            "priority": "low",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204


@pytest.mark.asyncio(loop_scope="session")
async def test_task_ownership(client):
    username_a, email_a = unique_user("owner")
    username_b, email_b = unique_user("other")

    token_a = await get_token(
        client,
        username_a,
        email_a,
    )

    token_b = await get_token(
        client,
        username_b,
        email_b,
    )

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token_a}"},
        json={
            "title": "Private task",
            "priority": "medium",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_can_access_other_users_task(client):
    user_username, user_email = unique_user("normal")
    admin_username, admin_email = unique_user("admin")

    user_token = await get_token(
        client,
        user_username,
        user_email,
    )

    admin_token = await get_token(
        client,
        admin_username,
        admin_email,
        role="admin",
    )

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "User task",
            "priority": "medium",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["owner_username"] == user_username


@pytest.mark.asyncio(loop_scope="session")
async def test_invalid_priority(client):
    username, email = unique_user("priority")

    token = await get_token(
        client,
        username,
        email,
    )

    response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Invalid priority task",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422