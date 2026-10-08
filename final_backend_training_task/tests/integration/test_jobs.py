import asyncio

import pytest

JOB_PAYLOAD = {
    "name": "Phase 4A Integration Test",
    "job_type": "report",
    "priority": "medium",
}


@pytest.mark.asyncio
async def test_gateway_creates_job(gateway_client, auth_headers):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json=JOB_PAYLOAD,
    )

    assert response.status_code in {200, 201}

    data = response.json()

    assert "id" in data
    assert data["name"] == JOB_PAYLOAD["name"]
    assert data["job_type"] == JOB_PAYLOAD["job_type"]
    assert data["priority"] == JOB_PAYLOAD["priority"]
    assert data["status"] in {
        "CREATED",
        "QUEUED",
        "PROCESSING",
        "COMPLETED",
    }


@pytest.mark.asyncio
async def test_job_stored_and_can_be_retrieved(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Database Persistence Test",
            "job_type": "report",
            "priority": "high",
        },
    )

    assert response.status_code in {200, 201}

    created = response.json()
    job_id = created["id"]

    response = await gateway_client.get(
        f"/api/v1/jobs/{job_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["name"] == "Database Persistence Test"


@pytest.mark.asyncio
async def test_job_eventually_completes(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Worker Completion Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code in {200, 201}

    job_id = response.json()["id"]

    final_status = None

    for _ in range(15):
        response = await gateway_client.get(
            f"/api/v1/jobs/{job_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200

        data = response.json()
        final_status = data["status"]

        if final_status == "COMPLETED":
            break

        if final_status == "FAILED":
            pytest.fail(f"Worker failed for job {job_id}")

        await asyncio.sleep(1)

    assert final_status == "COMPLETED"


@pytest.mark.asyncio
async def test_invalid_job_id_returns_404(
    gateway_client,
    auth_headers,
):
    invalid_id = 999999999

    response = await gateway_client.get(
        f"/api/v1/jobs/{invalid_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404
