import uuid

import pytest
from sqlalchemy import select
from app.core.redis import get_redis_client
from app.database import AsyncSessionLocal
from app.models.user import User


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


async def get_user_id(username):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User.id).where(User.username == username)
        )
        return result.scalar_one()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_task(client):
    username, email = unique_user("create")

    token = await get_token(
        client,
        username,
        email,
    )

    user_id = await get_user_id(username)

    response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Learn FastAPI",
            "description": "Complete Day 7 task",
            "priority": "high",
            "status": "pending",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert data["user_id"] == user_id
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_get_task_from_postgresql(client):
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
            "title": "PostgreSQL Task",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "PostgreSQL Task"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks_pagination(client):
    username, email = unique_user("pagination")

    token = await get_token(
        client,
        username,
        email,
    )

    for index in range(3):
        response = await client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": f"Pagination Task {index}",
                "priority": "medium",
                "status": "pending",
            },
        )

        assert response.status_code == 201

    response = await client.get(
        "/api/v1/tasks?page=1&page_size=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] >= 3
    assert len(data["items"]) <= 2


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
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated title",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated title"
    assert data["status"] == "in_progress"


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
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    delete_response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert delete_response.status_code == 204

    get_response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert get_response.status_code == 404


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
            "status": "pending",
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

    user_id = await get_user_id(user_username)

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "User task",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["user_id"] == user_id


@pytest.mark.asyncio(loop_scope="session")
async def test_status_history_after_update(client):
    username, email = unique_user("history")

    token = await get_token(
        client,
        username,
        email,
    )

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "History Task",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    update_response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "status": "completed",
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "completed"


@pytest.mark.asyncio(loop_scope="session")
async def test_redis_cache_created_after_get(client):
    username, email = unique_user("cache")

    token = await get_token(
        client,
        username,
        email,
    )

    user_id = await get_user_id(username)

    redis_client = get_redis_client()

    key = f"tasks:user:{user_id}:page:1:page_size:10"

    await redis_client.delete(key)

    response = await client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    cached_data = await redis_client.get(key)

    assert cached_data is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_redis_cache_hit(client):
    username, email = unique_user("cache_hit")

    token = await get_token(
        client,
        username,
        email,
    )

    user_id = await get_user_id(username)

    redis_client = get_redis_client()

    key = f"tasks:user:{user_id}:page:1:page_size:10"

    await redis_client.delete(key)

    first_response = await client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert first_response.status_code == 200
    assert await redis_client.get(key) is not None

    second_response = await client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert second_response.status_code == 200
    assert second_response.json() == first_response.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_redis_cache_invalidated_after_create(client):
    username, email = unique_user("cache_invalidate")

    token = await get_token(
        client,
        username,
        email,
    )

    user_id = await get_user_id(username)

    redis_client = get_redis_client()

    key = f"tasks:user:{user_id}:page:1:page_size:10"

    await redis_client.delete(key)

    cache_response = await client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert cache_response.status_code == 200
    assert await redis_client.get(key) is not None

    create_response = await client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Cache Invalidation Task",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    assert await redis_client.get(key) is None

@pytest.mark.asyncio
async def test_redis_cache_invalidated_after_update(client):
    username = f"cache_update_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    token = await get_token(client, username, email)

    user_id = await get_user_id(username)

    redis_client = get_redis_client()

    cache_key = (
        f"tasks:user:{user_id}:page:1:page_size:10"
    )

    await redis_client.delete(cache_key)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Populate cache
    response = await client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers=headers,
    )

    assert response.status_code == 200
    assert await redis_client.exists(cache_key)

    # Create task
    create_response = await client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Cache Update Test",
            "description": "Testing update invalidation",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Repopulate cache after create invalidation
    response = await client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers=headers,
    )

    assert response.status_code == 200
    assert await redis_client.exists(cache_key)

    # Update task
    update_response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={
            "status": "in_progress"
        },
    )

    assert update_response.status_code == 200

    # Cache should be invalidated
    assert not await redis_client.exists(cache_key)

@pytest.mark.asyncio
async def test_redis_cache_invalidated_after_delete(client):
    username = f"cache_delete_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    token = await get_token(client, username, email)

    user_id = await get_user_id(username)

    redis_client = get_redis_client()

    cache_key = (
        f"tasks:user:{user_id}:page:1:page_size:10"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    await redis_client.delete(cache_key)

    # Create task
    create_response = await client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Cache Delete Test",
            "description": "Testing delete invalidation",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Populate cache
    response = await client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers=headers,
    )

    assert response.status_code == 200
    assert await redis_client.exists(cache_key)

    # Delete task
    delete_response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    # Cache should be invalidated
    assert not await redis_client.exists(cache_key)