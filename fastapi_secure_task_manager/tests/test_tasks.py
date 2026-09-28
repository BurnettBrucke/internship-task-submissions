from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token(username: str, email: str, password: str, role: str = "user"):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    return response.json()["access_token"]


def test_create_task():
    token = get_token(
        "taskuser",
        "taskuser@example.com",
        "password123",
    )

    response = client.post(
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


def test_get_tasks():
    token = get_token(
        "getuser",
        "getuser@example.com",
        "password123",
    )

    client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test task",
            "priority": "medium",
        },
    )

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_task():
    token = get_token(
        "updateuser",
        "updateuser@example.com",
        "password123",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Old title",
            "priority": "low",
        },
    )

    task_id = create_response.json()["id"]

    response = client.put(
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


def test_delete_task():
    token = get_token(
        "deleteuser",
        "deleteuser@example.com",
        "password123",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Delete me",
            "priority": "low",
        },
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204


def test_task_ownership():
    token_a = get_token(
        "owneruser",
        "owneruser@example.com",
        "password123",
    )

    token_b = get_token(
        "otheruser",
        "otheruser@example.com",
        "password123",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token_a}"},
        json={
            "title": "Private task",
            "priority": "medium",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response.status_code == 403


def test_admin_can_access_other_users_task():
    user_token = get_token(
        "normaluser",
        "normaluser@example.com",
        "password123",
    )

    admin_token = get_token(
        "adminuser",
        "adminuser@example.com",
        "password123",
        role="admin",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "User task",
            "priority": "medium",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["owner_username"] == "normaluser"


def test_invalid_priority():
    token = get_token(
        "priorityuser",
        "priorityuser@example.com",
        "password123",
    )

    response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Invalid priority task",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422