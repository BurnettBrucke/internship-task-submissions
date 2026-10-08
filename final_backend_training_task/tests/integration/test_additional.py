import asyncio
import uuid

import pytest

from tests.conftest import test_settings


@pytest.mark.asyncio
async def test_invalid_login_returns_401(gateway_client):
    response = await gateway_client.post(
        "/api/v1/auth/login",
        json={
            "username": "wrong-user",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_missing_fields_returns_422(gateway_client):
    response = await gateway_client.post(
        "/api/v1/auth/login",
        json={},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_jwt_rejected(gateway_client):
    response = await gateway_client.get(
        "/api/v1/jobs/1",
        headers={
            "Authorization": "Bearer invalid.jwt.token",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_processing_missing_service_token(
    processing_client,
):
    response = await processing_client.post(
        "/internal/v1/jobs",
        json={
            "name": "Missing Token Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_processing_invalid_auth_scheme(
    processing_client,
):
    response = await processing_client.post(
        "/internal/v1/jobs",
        headers={
            "Authorization": "Basic some-token",
        },
        json={
            "name": "Invalid Scheme Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_processing_can_get_created_job(
    processing_client,
):
    response = await processing_client.post(
        "/internal/v1/jobs",
        headers={
            "Authorization": (f"Bearer {test_settings.processing_service_token}"),
        },
        json={
            "name": "Processing Get Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code in {200, 201}

    job_id = response.json()["id"]

    response = await processing_client.get(
        f"/internal/v1/jobs/{job_id}",
        headers={
            "Authorization": (f"Bearer {test_settings.processing_service_token}"),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["name"] == "Processing Get Test"


@pytest.mark.asyncio
async def test_processing_invalid_job_returns_404(
    processing_client,
):
    response = await processing_client.get(
        "/internal/v1/jobs/999999999",
        headers={
            "Authorization": (f"Bearer {test_settings.processing_service_token}"),
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_gateway_generates_correlation_id(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Generated Correlation Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code in {200, 201}

    correlation_id = response.headers.get("X-Correlation-ID")

    assert correlation_id
    assert len(correlation_id) > 10


@pytest.mark.asyncio
async def test_gateway_generates_request_id(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Generated Request Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code in {200, 201}

    request_id = response.headers.get("X-Request-ID")

    assert request_id
    assert len(request_id) > 10


@pytest.mark.parametrize(
    "priority",
    ["low", "medium", "high"],
)
@pytest.mark.asyncio
async def test_all_job_priorities(
    gateway_client,
    auth_headers,
    priority,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": f"Priority Test {priority}",
            "job_type": "report",
            "priority": priority,
        },
    )

    assert response.status_code in {200, 201}

    data = response.json()

    assert data["priority"] == priority


@pytest.mark.asyncio
async def test_different_idempotency_keys_create_different_jobs(
    gateway_client,
    auth_headers,
):
    payload = {
        "name": "Different Idempotency Keys",
        "job_type": "report",
        "priority": "medium",
    }

    response_1 = await gateway_client.post(
        "/api/v1/jobs",
        headers={
            **auth_headers,
            "Idempotency-Key": str(uuid.uuid4()),
        },
        json=payload,
    )

    response_2 = await gateway_client.post(
        "/api/v1/jobs",
        headers={
            **auth_headers,
            "Idempotency-Key": str(uuid.uuid4()),
        },
        json=payload,
    )

    assert response_1.status_code in {200, 201}
    assert response_2.status_code in {200, 201}

    assert response_1.json()["id"] != response_2.json()["id"]


@pytest.mark.asyncio
async def test_idempotency_replay_returns_same_job_after_completion(
    gateway_client,
    auth_headers,
):
    idempotency_key = str(uuid.uuid4())

    headers = {
        **auth_headers,
        "Idempotency-Key": idempotency_key,
    }

    payload = {
        "name": "Completed Idempotency Replay",
        "job_type": "report",
        "priority": "medium",
    }

    first = await gateway_client.post(
        "/api/v1/jobs",
        headers=headers,
        json=payload,
    )

    assert first.status_code in {200, 201}

    job_id = first.json()["id"]

    for _ in range(15):
        response = await gateway_client.get(
            f"/api/v1/jobs/{job_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200

        if response.json()["status"] == "COMPLETED":
            break

        await asyncio.sleep(1)

    second = await gateway_client.post(
        "/api/v1/jobs",
        headers=headers,
        json=payload,
    )

    assert second.status_code == 200
    assert second.json()["id"] == job_id
