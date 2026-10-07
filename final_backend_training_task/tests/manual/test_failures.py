import asyncio

import pytest


@pytest.mark.asyncio
async def test_processing_unavailable(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Processing Failure Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code in {502, 503}


@pytest.mark.asyncio
async def test_processing_timeout(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Processing Timeout Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code == 504


@pytest.mark.asyncio
async def test_worker_failure_results_in_failed(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Worker Failure Test",
            "job_type": "report",
            "priority": "high",
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

        final_status = response.json()["status"]

        if final_status in {"FAILED", "COMPLETED"}:
            break

        await asyncio.sleep(1)

    assert final_status == "FAILED"
