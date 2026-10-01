import asyncio

import pytest
from sqlalchemy import select

from app.models.task import Task
from app.models.task_history import TaskHistory
from tests.conftest import TestSessionLocal

def register_and_login(client, username, email, password="Password@123"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_task(client, token, title="Test Task"):
    return client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": title,
            "description": "Day 7 test task",
            "priority": "medium",
            "completed": False,
        },
    )


# 1. Create user and task in PostgreSQL
def test_01_create_user_and_task(client):
    token = register_and_login(
        client,
        "create_user",
        "create_user@example.com",
    )

    response = create_task(client, token)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Test Task"
    assert data["owner_id"] is not None


# 2. Retrieve task from DB
def test_02_retrieve_task(client):
    token = register_and_login(
        client,
        "retrieve_user",
        "retrieve@example.com",
    )

    create_response = create_task(client, token)

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Test Task"


# 3. Update task
def test_03_update_task(client):
    token = register_and_login(
        client,
        "update_user",
        "update@example.com",
    )

    create_response = create_task(client, token)

    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Updated Task",
            "priority": "high",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Updated Task"
    assert data["priority"] == "high"


# 4. Delete task
def test_04_delete_task(client):
    token = register_and_login(
        client,
        "delete_user",
        "delete@example.com",
    )

    create_response = create_task(client, token)

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


# 5. User cannot access another user's task
def test_05_user_cannot_access_another_users_task(client):
    owner_token = register_and_login(
        client,
        "owner_user",
        "owner@example.com",
    )

    other_token = register_and_login(
        client,
        "other_user",
        "other@example.com",
    )

    create_response = create_task(
        client,
        owner_token,
        title="Private Task",
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {other_token}",
        },
    )

    assert response.status_code == 403


# 6. Admin can access all tasks
def test_06_admin_can_access_all_tasks(client):
    owner_token = register_and_login(
        client,
        "task_owner",
        "task_owner@example.com",
    )

    create_response = create_task(
        client,
        owner_token,
        title="Owner Task",
    )

    task_id = create_response.json()["id"]

    admin_token = register_and_login(
        client,
        "admin_user",
        "admin@example.com",
    )

    async def make_admin():
        async with TestSessionLocal() as db:
            from app.models.user import User

            result = await db.execute(
                select(User).where(
                    User.email == "admin@example.com"
                )
            )

            user = result.scalar_one()
            user.role = "admin"

            await db.commit()

    asyncio.run(make_admin())

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


# 7. Task history is created after status update
def test_07_task_history_created_after_status_update(client):
    token = register_and_login(
        client,
        "history_user",
        "history@example.com",
    )

    create_response = create_task(client, token)

    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True

    async def get_history():
        async with TestSessionLocal() as db:
            result = await db.execute(
                select(TaskHistory).where(
                    TaskHistory.task_id == task_id
                )
            )

            return result.scalars().all()

    history = asyncio.run(get_history())

    assert len(history) == 1
    assert history[0].old_status == "pending"
    assert history[0].new_status == "completed"


# 8. Transaction rollback works
def test_08_transaction_rollback(client, monkeypatch):
    token = register_and_login(
        client,
        "rollback_user",
        "rollback@example.com",
    )

    create_response = create_task(client, token)

    task_id = create_response.json()["id"]

    async def failing_history(*args, **kwargs):
        raise RuntimeError("History insert failed")

    from app.repositories import task_history_repository

    monkeypatch.setattr(
        task_history_repository,
        "create_task_history",
        failing_history,
    )

    with pytest.raises(
        RuntimeError,
        match="History insert failed",
    ):
        client.put(
            f"/api/v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "completed": True,
            },
        )

    async def verify_rollback():
        async with TestSessionLocal() as db:
            task = await db.get(Task, task_id)

            result = await db.execute(
                select(TaskHistory).where(
                    TaskHistory.task_id == task_id
                )
            )

            return task, result.scalars().all()

    task, history = asyncio.run(verify_rollback())

    assert task.status == "pending"
    assert history == []


# 9. Redis cache is created after GET /tasks
def test_09_redis_cache_created_after_get(client, caplog):
    token = register_and_login(
        client,
        "redis_create_user",
        "redis_create@example.com",
    )

    create_task(client, token)

    caplog.clear()

    with caplog.at_level("INFO"):
        response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 200
    assert "Redis MISS" in caplog.text
    assert "Redis SET" in caplog.text


# 10. Cache hit returns expected response
def test_10_redis_cache_hit(client, caplog):
    token = register_and_login(
        client,
        "redis_hit_user",
        "redis_hit@example.com",
    )

    create_task(client, token)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    first_response = client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers=headers,
    )

    assert first_response.status_code == 200

    caplog.clear()

    with caplog.at_level("INFO"):
        second_response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers=headers,
        )

    assert second_response.status_code == 200
    assert "Redis HIT" in caplog.text

    assert first_response.json() == second_response.json()


# 11. Cache invalidates after create/update/delete
def test_11_cache_invalidates_after_create_update_delete(
    client,
    caplog,
):
    token = register_and_login(
        client,
        "cache_invalidation_user",
        "cache_invalidation@example.com",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Populate cache.
    create_response = create_task(
        client,
        token,
        title="Original Task",
    )

    task_id = create_response.json()["id"]

    client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers=headers,
    )

    # UPDATE invalidation.
    caplog.clear()

    with caplog.at_level("INFO"):
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            headers=headers,
            json={
                "title": "Updated Task",
            },
        )

    assert response.status_code == 200
    assert "Redis INVALIDATE" in caplog.text

    # Re-cache updated data.
    caplog.clear()

    client.get(
        "/api/v1/tasks?page=1&page_size=10",
        headers=headers,
    )

    # DELETE invalidation.
    caplog.clear()

    with caplog.at_level("INFO"):
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers=headers,
        )

    assert response.status_code == 204
    assert "Redis INVALIDATE" in caplog.text

    # CREATE invalidation.
    caplog.clear()

    with caplog.at_level("INFO"):
        response = create_task(
            client,
            token,
            title="New Task",
        )

    assert response.status_code == 201
    assert "Redis INVALIDATE" in caplog.text


# 12. Pagination returns correct page
def test_12_pagination_returns_correct_page(client):
    token = register_and_login(
        client,
        "pagination_user",
        "pagination@example.com",
    )

    for i in range(12):
        response = create_task(
            client,
            token,
            title=f"Task {i + 1}",
        )

        assert response.status_code == 201

    response = client.get(
        "/api/v1/tasks?page=1&page_size=5",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 5
    assert data["total"] == 12
    assert len(data["items"]) == 5

    response = client.get(
        "/api/v1/tasks?page=2&page_size=5",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["page_size"] == 5
    assert data["total"] == 12
    assert len(data["items"]) == 5


# 13. Duplicate email fails
def test_13_duplicate_email_fails(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "first_user",
            "email": "duplicate@example.com",
            "password": "Password@123",
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "second_user",
            "email": "duplicate@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code in (400, 409)


# 14. Invalid foreign key is handled
def test_14_invalid_foreign_key_is_handled():
    async def check_invalid_foreign_key():
        async with TestSessionLocal() as db:
            task = Task(
                user_id=999999999,
                title="Invalid FK Task",
                priority="medium",
                status="pending",
            )

            db.add(task)

            with pytest.raises(Exception):
                await db.flush()

            await db.rollback()

    asyncio.run(check_invalid_foreign_key())


# 15. Migration can be applied successfully
def test_15_migration_is_applied():
    import subprocess

    result = subprocess.run(
        ["alembic", "current"],
        capture_output=True,
        text=True,
        shell=True,
    )

    assert result.returncode == 0
    assert "head" in result.stdout