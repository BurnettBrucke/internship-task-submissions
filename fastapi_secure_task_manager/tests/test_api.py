import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.data.store import users, tasks


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    users.clear()
    tasks.clear()
    yield
    users.clear()
    tasks.clear()


def register_user(
    username="testuser",
    email="test@example.com",
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
    username="testuser",
    password="StrongPass@123",
):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    return response


def get_token(username="testuser"):
    response = login_user(username=username)

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def create_task(token, title="Test Task"):
    return client.post(
        "/api/v1/tasks",
        headers=auth_headers(token),
        json={
            "title": title,
            "description": "Test description",
            "priority": "high",
            "completed": False,
        },
    )


# ---------------------------------------------------------
# AUTHENTICATION TESTS
# ---------------------------------------------------------


def test_register_new_user_successfully():
    response = register_user()

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"


def test_duplicate_username_should_fail():
    first_response = register_user()

    assert first_response.status_code == 201

    second_response = register_user(
        email="another@example.com"
    )

    assert second_response.status_code == 409


def test_invalid_email_should_fail():
    response = register_user(
        email="invalid-email"
    )

    assert response.status_code == 422


def test_short_password_should_fail():
    response = register_user(
        password="123"
    )

    assert response.status_code == 422


def test_correct_login_returns_token():
    register_user()

    response = login_user()

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


def test_wrong_password_returns_401():
    register_user()

    response = login_user(
        password="WrongPassword@123"
    )

    assert response.status_code == 401


def test_get_me_with_valid_token():
    register_user()

    token = get_token()

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_protected_endpoint_without_token_returns_401():
    response = client.get(
        "/api/v1/tasks"
    )

    assert response.status_code == 401


# ---------------------------------------------------------
# TASK TESTS
# ---------------------------------------------------------


def test_user_creates_task():
    register_user()

    token = get_token()

    response = create_task(token)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert data["owner_id"] == 1


def test_user_views_own_tasks():
    register_user()

    token = get_token()

    create_task(token)

    response = client.get(
        "/api/v1/tasks",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Test Task"


def test_user_cannot_update_another_users_task():
    register_user(
        username="user1",
        email="user1@example.com",
    )

    token1 = get_token("user1")

    task_response = create_task(
        token1,
        title="User 1 Task",
    )

    task_id = task_response.json()["id"]

    register_user(
        username="user2",
        email="user2@example.com",
    )

    token2 = get_token("user2")

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token2),
        json={
            "title": "Trying To Change",
            "description": "Unauthorized update",
            "priority": "low",
            "completed": False,
        },
    )

    assert response.status_code == 403


def test_admin_can_view_another_users_task():
    register_user(
        username="normaluser",
        email="normal@example.com",
        role="user",
    )

    user_token = get_token("normaluser")

    task_response = create_task(
        user_token,
        title="Normal User Task",
    )

    task_id = task_response.json()["id"]

    register_user(
        username="admin",
        email="admin@example.com",
        role="admin",
    )

    admin_token = get_token("admin")

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Normal User Task"


def test_admin_can_delete_another_users_task():
    register_user(
        username="normaluser",
        email="normal@example.com",
        role="user",
    )

    user_token = get_token("normaluser")

    task_response = create_task(
        user_token,
        title="Task To Delete",
    )

    task_id = task_response.json()["id"]

    register_user(
        username="admin",
        email="admin@example.com",
        role="admin",
    )

    admin_token = get_token("admin")

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 204


def test_invalid_priority_should_fail_validation():
    register_user()

    token = get_token()

    response = client.post(
        "/api/v1/tasks",
        headers=auth_headers(token),
        json={
            "title": "Invalid Priority Task",
            "description": "Testing validation",
            "priority": "urgent",
            "completed": False,
        },
    )

    assert response.status_code == 422


def test_unknown_task_id_returns_404():
    register_user()

    token = get_token()

    response = client.get(
        "/api/v1/tasks/9999",
        headers=auth_headers(token),
    )

    assert response.status_code == 404