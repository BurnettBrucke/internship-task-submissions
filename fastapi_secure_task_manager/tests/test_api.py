import pytest

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.cache.redis import redis_client
from app.models.task import Task
from app.models.task_history import TaskHistory
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.services import task_service


# =========================================================
# TEST HELPERS
# =========================================================


async def register_user(
    client,
    username="testuser",
    email="test@example.com",
    password="StrongPass@123",
):
    return await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )


async def login_user(
    client,
    username="testuser",
    password="StrongPass@123",
):
    return await client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )


async def get_token(
    client,
    username="testuser",
):
    response = await login_user(
        client,
        username=username,
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
    }


async def create_task(
    client,
    token,
    title="Test Task",
    status="pending",
):
    return await client.post(
        "/api/v1/tasks",
        headers=auth_headers(token),
        json={
            "title": title,
            "description": "Test description",
            "priority": "high",
            "status": status,
        },
    )


async def get_current_user_id(client, token):
    response = await client.get(
        "/api/v1/auth/me",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    return response.json()["id"]


# =========================================================
# AUTHENTICATION
# =========================================================


@pytest.mark.asyncio
async def test_register_user_in_postgresql(client):
    response = await register_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_duplicate_username_fails(client):
    first = await register_user(client)

    assert first.status_code == 201

    second = await register_user(
        client,
        email="another@example.com",
    )

    assert second.status_code == 409


@pytest.mark.asyncio
async def test_duplicate_email_fails(client):
    first = await register_user(client)

    assert first.status_code == 201

    second = await register_user(
        client,
        username="differentuser",
    )

    assert second.status_code == 409


@pytest.mark.asyncio
async def test_invalid_email_fails(client):
    response = await register_user(
        client,
        email="invalid-email",
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_returns_jwt(client):
    await register_user(client)

    response = await login_user(client)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(client):
    await register_user(client)

    token = await get_token(client)

    response = await client.get(
        "/api/v1/auth/me",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"


# =========================================================
# TASK CRUD
# =========================================================


@pytest.mark.asyncio
async def test_create_task_in_postgresql(client):
    await register_user(client)

    token = await get_token(client)

    response = await create_task(
        client,
        token,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Task"
    assert isinstance(data["user_id"], int)
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_retrieve_task_from_postgresql(client):
    await register_user(client)

    token = await get_token(client)

    task_response = await create_task(
        client,
        token,
    )

    assert task_response.status_code == 201

    task_id = task_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Test Task"


@pytest.mark.asyncio
async def test_update_task(client):
    await register_user(client)

    token = await get_token(client)

    task_response = await create_task(
        client,
        token,
    )

    task_id = task_response.json()["id"]

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token),
        json={
            "title": "Updated Task",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Task"
    assert data["status"] == "in_progress"


@pytest.mark.asyncio
async def test_delete_task(client):
    await register_user(client)

    token = await get_token(client)

    task_response = await create_task(
        client,
        token,
    )

    task_id = task_response.json()["id"]

    response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 204

    get_response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token),
    )

    assert get_response.status_code == 404


# =========================================================
# AUTHORIZATION
# =========================================================


@pytest.mark.asyncio
async def test_user_cannot_access_another_users_task(client):
    await register_user(
        client,
        username="user1",
        email="user1@example.com",
    )

    token1 = await get_token(
        client,
        username="user1",
    )

    task_response = await create_task(
        client,
        token1,
        title="User 1 Task",
    )

    task_id = task_response.json()["id"]

    await register_user(
        client,
        username="user2",
        email="user2@example.com",
    )

    token2 = await get_token(
        client,
        username="user2",
    )

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token2),
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_access_all_tasks(
    client,
    db_session,
):
    await register_user(
        client,
        username="normaluser",
        email="normal@example.com",
    )

    user_token = await get_token(
        client,
        username="normaluser",
    )

    task_response = await create_task(
        client,
        user_token,
        title="Normal User Task",
    )

    task_id = task_response.json()["id"]

    await register_user(
        client,
        username="admin",
        email="admin@example.com",
    )

    # Promote the test user directly in the database.
    # This avoids relying on public registration to create
    # privileged accounts.
    await db_session.execute(
        update(User)
        .where(User.username == "admin")
        .values(role="admin")
    )

    await db_session.commit()

    admin_token = await get_token(
        client,
        username="admin",
    )

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Normal User Task"


# =========================================================
# TASK HISTORY
# =========================================================


@pytest.mark.asyncio
async def test_task_history_created_after_status_change(
    client,
    db_session,
):
    await register_user(client)

    token = await get_token(client)

    task_response = await create_task(
        client,
        token,
    )

    task_id = task_response.json()["id"]

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token),
        json={
            "status": "completed",
        },
    )

    assert response.status_code == 200

    result = await db_session.execute(
        select(TaskHistory)
        .where(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.id)
    )

    history = result.scalar_one_or_none()

    assert history is not None
    assert history.old_status == "pending"
    assert history.new_status == "completed"


# =========================================================
# PAGINATION
# =========================================================


@pytest.mark.asyncio
async def test_pagination(client):
    await register_user(client)

    token = await get_token(client)

    for index in range(15):
        response = await create_task(
            client,
            token,
            title=f"Task {index}",
        )

        assert response.status_code == 201

    response = await client.get(
        "/api/v1/tasks?page=2&page_size=10",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["page_size"] == 10
    assert data["total"] == 15
    assert len(data["items"]) == 5


# =========================================================
# INVALID FOREIGN KEY
# =========================================================


@pytest.mark.asyncio
async def test_invalid_foreign_key_is_rejected(
    client,
    db_session,
):
    await register_user(client)

    token = await get_token(client)

    task_response = await create_task(
        client,
        token,
    )

    task_id = task_response.json()["id"]

    max_user_result = await db_session.execute(
        select(User.id)
        .order_by(User.id.desc())
        .limit(1)
    )

    max_user_id = max_user_result.scalar_one()

    invalid_user_id = max_user_id + 1

    history = TaskHistory(
        task_id=task_id,
        changed_by=invalid_user_id,
        old_status="pending",
        new_status="completed",
    )

    db_session.add(history)

    with pytest.raises(IntegrityError):
        await db_session.flush()

    await db_session.rollback()


# =========================================================
# TRANSACTION ROLLBACK
# =========================================================


@pytest.mark.asyncio
async def test_transaction_rolls_back_task_update(
    client,
    db_session,
    monkeypatch,
):
    await register_user(client)

    token = await get_token(client)

    task_response = await create_task(
        client,
        token,
    )

    task_id = task_response.json()["id"]

    user_result = await db_session.execute(
        select(User).where(User.username == "testuser")
    )

    current_user = user_result.scalar_one()

    max_user_result = await db_session.execute(
        select(User.id)
        .order_by(User.id.desc())
        .limit(1)
    )

    max_user_id = max_user_result.scalar_one()

    invalid_user_id = max_user_id + 1

    async def failing_history_create(
        self,
        history,
    ):
        history.changed_by = invalid_user_id

        self.session.add(history)

        await self.session.flush()

    monkeypatch.setattr(
        task_service.TaskHistoryRepository,
        "create",
        failing_history_create,
    )

    with pytest.raises(IntegrityError):
        await task_service.update_task(
            session=db_session,
            task_id=task_id,
            current_user=current_user,
            status="completed",
        )

    result = await db_session.execute(
        select(Task).where(Task.id == task_id)
    )

    rolled_back_task = result.scalar_one()

    assert rolled_back_task.status == "pending"


# =========================================================
# SECURITY REGRESSION
# =========================================================


@pytest.mark.asyncio
async def test_public_registration_cannot_create_admin(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "adminattempt",
            "email": "adminattempt@example.com",
            "password": "password123",
            "role": "admin",
        },
    )

    assert response.status_code == 422


# =========================================================
# REDIS CACHE
# =========================================================


@pytest.mark.asyncio
async def test_tasks_cache_is_created(client):
    await register_user(client)

    token = await get_token(client)

    user_id = await get_current_user_id(
        client,
        token,
    )

    response = await client.get(
        "/api/v1/tasks",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    cached_data = await redis_client.get(
        f"tasks:user:{user_id}"
    )

    assert cached_data is not None


@pytest.mark.asyncio
async def test_tasks_cache_hit(
    client,
    monkeypatch,
):
    await register_user(client)

    token = await get_token(client)

    user_id = await get_current_user_id(
        client,
        token,
    )

    headers = auth_headers(token)

    # First request populates Redis.
    first_response = await client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert first_response.status_code == 200

    assert await redis_client.get(
        f"tasks:user:{user_id}"
    ) is not None

    async def fail_count(*args, **kwargs):
        raise AssertionError(
            "Database count_tasks should not run on cache HIT"
        )

    async def fail_list(*args, **kwargs):
        raise AssertionError(
            "Database list_tasks should not run on cache HIT"
        )

    monkeypatch.setattr(
        TaskRepository,
        "count_tasks",
        fail_count,
    )

    monkeypatch.setattr(
        TaskRepository,
        "list_tasks",
        fail_list,
    )

    # Second request must come from Redis.
    second_response = await client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert second_response.status_code == 200
    assert second_response.json() == first_response.json()


@pytest.mark.asyncio
async def test_create_task_invalidates_tasks_cache(client):
    await register_user(client)

    token = await get_token(client)

    user_id = await get_current_user_id(
        client,
        token,
    )

    headers = auth_headers(token)

    # Populate cache.
    response = await client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert response.status_code == 200

    assert await redis_client.get(
        f"tasks:user:{user_id}"
    ) is not None

    # Create task.
    create_response = await client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Redis Create Test",
            "description": "Testing POST cache invalidation",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    # POST must invalidate the user's task cache.
    assert await redis_client.get(
        f"tasks:user:{user_id}"
    ) is None


@pytest.mark.asyncio
async def test_update_task_invalidates_tasks_cache(client):
    await register_user(client)

    token = await get_token(client)

    user_id = await get_current_user_id(
        client,
        token,
    )

    headers = auth_headers(token)

    create_response = await client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Redis Update Test",
            "description": "Testing PUT cache invalidation",
            "priority": "medium",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Populate cache.
    list_response = await client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert list_response.status_code == 200

    assert await redis_client.get(
        f"tasks:user:{user_id}"
    ) is not None

    # Update task.
    update_response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={
            "status": "in_progress",
        },
    )

    assert update_response.status_code == 200

    # PUT must invalidate the cache.
    assert await redis_client.get(
        f"tasks:user:{user_id}"
    ) is None


@pytest.mark.asyncio
async def test_delete_task_invalidates_tasks_cache(client):
    await register_user(client)

    token = await get_token(client)

    user_id = await get_current_user_id(
        client,
        token,
    )

    headers = auth_headers(token)

    create_response = await client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Redis Delete Test",
            "description": "Testing DELETE cache invalidation",
            "priority": "low",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Populate cache.
    list_response = await client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert list_response.status_code == 200

    assert await redis_client.get(
        f"tasks:user:{user_id}"
    ) is not None

    # Delete task.
    delete_response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    # DELETE must invalidate the cache.
    assert await redis_client.get(
        f"tasks:user:{user_id}"
    ) is None