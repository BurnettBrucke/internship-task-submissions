import uuid

import pytest


@pytest.mark.asyncio
async def test_duplicate_idempotency_key_creates_one_job(
    gateway_client,
    auth_headers,
):
    idempotency_key = f"test-{uuid.uuid4()}"

    payload = {
        "name": "Idempotency Test",
        "job_type": "report",
        "priority": "low",
    }

    headers = {
        **auth_headers,
        "Idempotency-Key": idempotency_key,
    }

    first_response = await gateway_client.post(
        "/api/v1/jobs",
        headers=headers,
        json=payload,
    )

    assert first_response.status_code in {200, 201}

    first_job = first_response.json()

    second_response = await gateway_client.post(
        "/api/v1/jobs",
        headers=headers,
        json=payload,
    )

    assert second_response.status_code == 200

    second_job = second_response.json()

    assert second_job["id"] == first_job["id"]


@pytest.mark.asyncio
async def test_same_idempotency_key_different_payload_returns_409(
    gateway_client,
    auth_headers,
):
    idempotency_key = f"test-{uuid.uuid4()}"

    headers = {
        **auth_headers,
        "Idempotency-Key": idempotency_key,
    }

    first_payload = {
        "name": "Original Job",
        "job_type": "report",
        "priority": "low",
    }

    second_payload = {
        "name": "Different Job",
        "job_type": "report",
        "priority": "high",
    }

    first_response = await gateway_client.post(
        "/api/v1/jobs",
        headers=headers,
        json=first_payload,
    )

    assert first_response.status_code in {200, 201}

    second_response = await gateway_client.post(
        "/api/v1/jobs",
        headers=headers,
        json=second_payload,
    )

    assert second_response.status_code == 409
