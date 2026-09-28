from fastapi.testclient import TestClient

from app.main import app
from app.data.store import users, tasks


client = TestClient(app)


def setup_function():
    users.clear()
    tasks.clear()


def register_and_login(
    username,
    email,
    password="StrongPass@123",
    role="user"
):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response.json()["access_token"]


# 9. User creates a task

def test_user_creates_task():
    token = register_and_login(
        "user1",
        "user1@example.com"
    )

    response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Learn FastAPI",
            "description": "Complete Day 6 task",
            "priority": "high",
            "completed": False
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["owner_id"] == 1


# 10. User views own tasks

def test_user_views_own_tasks():
    token = register_and_login(
        "user1",
        "user1@example.com"
    )

    client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "My Task",
            "description": "My task description",
            "priority": "medium",
            "completed": False
        }
    )

    response = client.get(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "My Task"


# 11. User cannot update another user's task

def test_user_cannot_update_another_users_task():
    user1_token = register_and_login(
        "user1",
        "user1@example.com"
    )

    client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {user1_token}"
        },
        json={
            "title": "User 1 Task",
            "description": "Private task",
            "priority": "high",
            "completed": False
        }
    )

    user2_token = register_and_login(
        "user2",
        "user2@example.com"
    )

    response = client.put(
        "/api/v1/tasks/1",
        headers={
            "Authorization": f"Bearer {user2_token}"
        },
        json={
            "title": "Trying to change task"
        }
    )

    assert response.status_code == 403


# 12. Admin can view another user's task

def test_admin_can_view_another_users_task():
    user_token = register_and_login(
        "user1",
        "user1@example.com"
    )

    client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "title": "User Task",
            "description": "Task owned by user",
            "priority": "low",
            "completed": False
        }
    )

    admin_token = register_and_login(
        "admin1",
        "admin1@example.com",
        role="admin"
    )

    response = client.get(
        "/api/v1/tasks/1",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "User Task"


# 13. Admin can delete another user's task

def test_admin_can_delete_another_users_task():
    user_token = register_and_login(
        "user1",
        "user1@example.com"
    )

    client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "title": "Delete Me",
            "description": "Admin should delete this",
            "priority": "medium",
            "completed": False
        }
    )

    admin_token = register_and_login(
        "admin1",
        "admin1@example.com",
        role="admin"
    )

    response = client.delete(
        "/api/v1/tasks/1",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 204
    assert len(tasks) == 0


# 14. Invalid priority should fail validation

def test_invalid_priority():
    token = register_and_login(
        "user1",
        "user1@example.com"
    )

    response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Invalid Priority",
            "description": "Testing validation",
            "priority": "urgent",
            "completed": False
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


# 15. Unknown task ID returns 404

def test_unknown_task_id():
    token = register_and_login(
        "user1",
        "user1@example.com"
    )

    response = client.get(
        "/api/v1/tasks/999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["code"] == "TASK_NOT_FOUND"