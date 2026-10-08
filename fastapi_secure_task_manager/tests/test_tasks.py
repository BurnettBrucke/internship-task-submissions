import pytest
import asyncio

from sqlalchemy import select

from app.models.task import Task
from app.models.task_history import TaskHistory
from tests.conftest import TestSessionLocal
from app.models.task import Task


def register_and_login(
    client,
    username,
    email,
    password="StrongPass@123",
    role="user",
):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def create_task(
    client,
    token,
    title="Test Task",
    description="Test description",
    priority="medium",
    completed=False,
):
    return client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed,
        },
    )


# 9. User creates a task
def test_user_creates_task(client):
    token = register_and_login(
        client,
        "user1",
        "user1@example.com",
    )

    response = create_task(
        client,
        token,
        title="Learn FastAPI",
        description="Complete Day 7 task",
        priority="high",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Learn FastAPI"
    assert data["owner_id"] is not None
    assert data["completed"] is False


# 10. User views own tasks
def test_user_views_own_tasks(client):
    token = register_and_login(
        client,
        "user1",
        "user1@example.com",
    )

    create_task(
        client,
        token,
        title="My Task",
        description="My task description",
        priority="medium",
    )

    response = client.get(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "My Task"


# 11. User cannot update another user's task
def test_user_cannot_update_another_users_task(client):
    user1_token = register_and_login(
        client,
        "user1",
        "user1@example.com",
    )

    create_response = create_task(
        client,
        user1_token,
        title="User 1 Task",
        description="Private task",
        priority="high",
    )

    task_id = create_response.json()["id"]

    user2_token = register_and_login(
        client,
        "user2",
        "user2@example.com",
    )

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user2_token}",
        },
        json={
            "title": "Trying to change task",
        },
    )

    assert response.status_code == 403


# 12. Admin can view another user's task
def test_admin_can_view_another_users_task(client):
    user_token = register_and_login(
        client,
        "user1",
        "user1@example.com",
    )

    create_response = create_task(
        client,
        user_token,
        title="User Task",
        description="Task owned by user",
        priority="low",
    )
    created_task = create_response.json()

    task_id = created_task["id"]
    owner_id = created_task["owner_id"]

    task_id = create_response.json()["id"]

    admin_token = register_and_login(
        client,
        "admin1",
        "admin1@example.com",
        role="admin",
    )

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "User Task"
    assert data["owner_id"] == owner_id


# 13. Admin can delete another user's task
def test_admin_can_delete_another_users_task(client):
    user_token = register_and_login(
        client,
        "user1",
        "user1@example.com",
    )

    create_response = create_task(
        client,
        user_token,
        title="Delete Me",
        description="Admin should delete this",
        priority="medium",
    )

    task_id = create_response.json()["id"]

    admin_token = register_and_login(
        client,
        "admin1",
        "admin1@example.com",
        role="admin",
    )

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 204

    # Verify through the API instead of the old in-memory `tasks` list.
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 404


# 14. Invalid priority should fail validation
def test_invalid_priority(client):
    token = register_and_login(
        client,
        "user1",
        "user1@example.com",
    )

    response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Invalid Priority",
            "description": "Testing validation",
            "priority": "urgent",
            "completed": False,
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


# 15. Unknown task ID returns 404
def test_unknown_task_id(client):
    token = register_and_login(
        client,
        "user1",
        "user1@example.com",
    )

    response = client.get(
        "/api/v1/tasks/999999",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["code"] == "TASK_NOT_FOUND"


def test_task_pagination(client):
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
            description=f"Pagination task {i + 1}",
            priority="medium",
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


def test_tasks_redis_cache_miss_then_hit(client, caplog):
    token = register_and_login(
        client,
        "redis_user",
        "redis@example.com",
    )

    response = create_task(
        client,
        token,
        title="Redis Cache Task",
        description="Testing Redis cache",
        priority="high",
    )

    assert response.status_code == 201

    with caplog.at_level("INFO"):
        first_response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert first_response.status_code == 200
    assert "Redis MISS" in caplog.text

    caplog.clear()

    with caplog.at_level("INFO"):
        second_response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert second_response.status_code == 200
    assert "Redis HIT" in caplog.text

    assert first_response.json() == second_response.json()


def test_tasks_cache_invalidation_after_create(client, caplog):
    token = register_and_login(
        client,
        "cache_user",
        "cache@example.com",
    )

    # First request populates Redis cache.
    with caplog.at_level("INFO"):
        response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 200
    assert "Redis MISS" in caplog.text

    caplog.clear()

    # Second request should use Redis.
    with caplog.at_level("INFO"):
        response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 200
    assert "Redis HIT" in caplog.text

    caplog.clear()

    # Creating a task must invalidate the user's cache.
    response = create_task(
        client,
        token,
        title="New Cached Task",
        description="Testing invalidation",
        priority="medium",
    )

    assert response.status_code == 201
    assert "Redis INVALIDATE" in caplog.text

    caplog.clear()

    # Next GET must be a MISS because cache was invalidated.
    with caplog.at_level("INFO"):
        response = client.get(
            "/api/v1/tasks?page=1&page_size=10",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 200
    assert "Redis MISS" in caplog.text

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1

def test_task_status_update_rolls_back_when_history_fails(
    client,
    monkeypatch,
):
    token = register_and_login(
        client,
        "rollback_user",
        "rollback@example.com",
    )

    create_response = create_task(
        client,
        token,
        title="Rollback Task",
        description="Testing transaction rollback",
        priority="high",
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    async def failing_history(*args, **kwargs):
        raise RuntimeError("History insert failed")

    from app.repositories import task_history_repository

    monkeypatch.setattr(
        task_history_repository,
        "create_task_history",
        failing_history,
    )

    with pytest.raises(RuntimeError, match="History insert failed"):
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

            history = await db.execute(
                select(TaskHistory).where(
                    TaskHistory.task_id == task_id
                )
            )

            return task, history.scalars().all()

    task, history_records = asyncio.run(verify_rollback())

    assert task is not None
    assert task.status == "pending"
    assert history_records == []