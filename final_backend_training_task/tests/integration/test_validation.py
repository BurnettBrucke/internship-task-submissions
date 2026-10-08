import pytest


@pytest.mark.asyncio
async def test_invalid_job_payload(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "",
            "job_type": "invalid",
            "priority": "invalid",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_job_fields(
    gateway_client,
    auth_headers,
):
    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=auth_headers,
        json={
            "name": "Incomplete Job",
        },
    )

    assert response.status_code == 422
