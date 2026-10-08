import uuid

import httpx
import pytest


GATEWAY_URL = "http://127.0.0.1:8000"
PROCESSING_URL = "http://127.0.0.1:8001"


@pytest.fixture
def client():
    return httpx.Client(timeout=10.0)


@pytest.fixture
def auth_token(client):
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    register_response = client.post(
        f"{GATEWAY_URL}/api/v1/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        f"{GATEWAY_URL}/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


# ---------------------------------------------------------
# 1. Gateway Health
# ---------------------------------------------------------

def test_gateway_health(client):
    response = client.get(f"{GATEWAY_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ---------------------------------------------------------
# 2. Gateway Readiness
# ---------------------------------------------------------

def test_gateway_ready(client):
    response = client.get(f"{GATEWAY_URL}/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


# ---------------------------------------------------------
# 3. Processing Health
# ---------------------------------------------------------

def test_processing_health(client):
    response = client.get(f"{PROCESSING_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ---------------------------------------------------------
# 4. Processing Readiness
# ---------------------------------------------------------

def test_processing_ready(client):
    response = client.get(f"{PROCESSING_URL}/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


# ---------------------------------------------------------
# 5. User Registration
# ---------------------------------------------------------

def test_user_registration(client):
    username = f"user_{uuid.uuid4().hex[:8]}"

    response = client.post(
        f"{GATEWAY_URL}/api/v1/auth/register",
        json={
            "username": username,
            "password": "Test@12345",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == username
    assert response.json()["role"] == "user"


# ---------------------------------------------------------
# 6. User Login
# ---------------------------------------------------------

def test_user_login(client):
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    register_response = client.post(
        f"{GATEWAY_URL}/api/v1/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        f"{GATEWAY_URL}/api/v1/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"


# ---------------------------------------------------------
# 7. Create Job
# ---------------------------------------------------------

def test_create_job(client, auth_token):
    response = client.post(
        f"{GATEWAY_URL}/api/v1/jobs",
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
        json={
            "name": "Integration Test Job",
            "job_type": "report",
            "priority": "high",
        },
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["status"] == "QUEUED"


# ---------------------------------------------------------
# 8. Get Existing Job
# ---------------------------------------------------------

def test_get_existing_job(client, auth_token):
    create_response = client.post(
        f"{GATEWAY_URL}/api/v1/jobs",
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
        json={
            "name": "Get Job Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    get_response = client.get(
        f"{GATEWAY_URL}/api/v1/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == job_id


# ---------------------------------------------------------
# 9. Get Missing Job
# ---------------------------------------------------------

def test_get_missing_job(client, auth_token):
    fake_job_id = str(uuid.uuid4())

    response = client.get(
        f"{GATEWAY_URL}/api/v1/jobs/{fake_job_id}",
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "JOB_NOT_FOUND"


# ---------------------------------------------------------
# 10. Missing JWT
# ---------------------------------------------------------

def test_missing_jwt(client):
    response = client.post(
        f"{GATEWAY_URL}/api/v1/jobs",
        json={
            "name": "Unauthorized Job",
            "job_type": "report",
            "priority": "high",
        },
    )

    assert response.status_code == 401
    assert response.json()["error"]["request_id"]


# ---------------------------------------------------------
# 11. Idempotency - Same Key + Same Payload
# ---------------------------------------------------------

def test_idempotency_same_key_same_payload(client, auth_token):
    idempotency_key = f"test-{uuid.uuid4()}"

    payload = {
        "name": "Idempotency Same Test",
        "job_type": "report",
        "priority": "high",
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Idempotency-Key": idempotency_key,
    }

    first_response = client.post(
        f"{GATEWAY_URL}/api/v1/jobs",
        headers=headers,
        json=payload,
    )

    assert first_response.status_code == 201

    first_job_id = first_response.json()["id"]

    second_response = client.post(
        f"{GATEWAY_URL}/api/v1/jobs",
        headers=headers,
        json=payload,
    )

    assert second_response.status_code == 201

    second_job_id = second_response.json()["id"]

    assert first_job_id == second_job_id


# ---------------------------------------------------------
# 12. Idempotency - Same Key + Different Payload
# ---------------------------------------------------------

def test_idempotency_different_payload(client, auth_token):
    idempotency_key = f"test-{uuid.uuid4()}"

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Idempotency-Key": idempotency_key,
    }

    first_response = client.post(
        f"{GATEWAY_URL}/api/v1/jobs",
        headers=headers,
        json={
            "name": "First Job",
            "job_type": "report",
            "priority": "high",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        f"{GATEWAY_URL}/api/v1/jobs",
        headers=headers,
        json={
            "name": "Different Job",
            "job_type": "report",
            "priority": "low",
        },
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["error"]["code"]
        == "IDEMPOTENCY_CONFLICT"
    )