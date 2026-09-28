from fastapi.testclient import TestClient

from app.main import app
from app.data.store import users_db, tasks_db


client = TestClient(app)


def setup_function():
    users_db.clear()
    tasks_db.clear()

    import app.data.store as store
    store.next_task_id = 1


def register_and_login(
    username: str,
    email: str,
    password: str,
    role: str = "user",
):
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
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Learn FastAPI",
            "description": "Study authentication",
            "priority": "high",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert data["owner_username"] == "user1"


def test_list_tasks_returns_own_tasks():
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "My Task",
            "priority": "medium",
            "completed": False,
        },
    )

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["owner_username"] == "user1"


def test_task_requires_authentication():
    response = client.get("/api/v1/tasks")

    assert response.status_code == 401


def test_get_task():
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Task",
            "priority": "low",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_task_not_found():
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    response = client.get(
        "/api/v1/tasks/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_update_task():
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Old Title",
            "priority": "low",
        },
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Title",
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Title"
    assert data["completed"] is True


def test_delete_task():
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Task To Delete",
            "priority": "medium",
        },
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204


def test_user_cannot_access_other_users_task():
    token_user1 = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    token_user2 = register_and_login(
        "user2",
        "user2@example.com",
        "UserTwo@123",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token_user2}"},
        json={
            "title": "User 2 Private Task",
            "priority": "high",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_user1}"},
    )

    assert response.status_code == 403


def test_admin_can_access_other_users_task():
    user_token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    admin_token = register_and_login(
        "admin",
        "admin@example.com",
        "AdminPass@123",
        role="admin",
    )

    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "User Private Task",
            "priority": "high",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_invalid_task_priority():
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Invalid Priority Task",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422


def test_empty_task_title():
    token = register_and_login(
        "user1",
        "user1@example.com",
        "UserOne@123",
    )

    response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "",
            "priority": "medium",
        },
    )

    assert response.status_code == 422

# ============================================================
# USER CANNOT UPDATE ANOTHER USER'S TASK
# ============================================================

def test_user_cannot_update_other_users_task():
    # Create first user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "owner_user",
            "email": "owner@example.com",
            "password": "password123",
            "role": "user",
        },
    )

    assert response.status_code == 201

    # Login first user
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "owner_user",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    owner_token = response.json()["access_token"]

    # Owner creates a task
    response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "title": "Owner Task",
            "description": "Private task",
            "priority": "medium",
            "completed": False,
        },
    )

    assert response.status_code == 201
    task_id = response.json()["id"]

    # Create second user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "other_user",
            "email": "other@example.com",
            "password": "password123",
            "role": "user",
        },
    )

    assert response.status_code == 201

    # Login second user
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "other_user",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    other_token = response.json()["access_token"]

    # Second user tries to update owner's task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {other_token}"
        },
        json={
            "title": "Unauthorized Update",
        },
    )

    assert response.status_code == 403

# ============================================================
# ADMIN CAN DELETE ANOTHER USER'S TASK
# ============================================================

def test_admin_can_delete_other_users_task():
    # Create normal user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "task_owner",
            "email": "taskowner@example.com",
            "password": "password123",
            "role": "user",
        },
    )

    assert response.status_code == 201

    # Login normal user
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "task_owner",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    user_token = response.json()["access_token"]

    # User creates task
    response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "title": "Task To Be Deleted",
            "description": "Admin will delete this",
            "priority": "low",
            "completed": False,
        },
    )

    assert response.status_code == 201
    task_id = response.json()["id"]

    # Create admin
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "admin_delete",
            "email": "admindelete@example.com",
            "password": "password123",
            "role": "admin",
        },
    )

    assert response.status_code == 201

    # Login admin
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin_delete",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    admin_token = response.json()["access_token"]

    # Admin deletes another user's task
    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 204

    # Verify task no longer exists
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 404