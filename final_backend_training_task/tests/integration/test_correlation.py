import uuid

import pytest


@pytest.mark.asyncio
async def test_correlation_id_propagation(
    gateway_client,
    auth_headers,
):
    correlation_id = str(uuid.uuid4())

    headers = {
        **auth_headers,
        "X-Correlation-ID": correlation_id,
    }

    response = await gateway_client.post(
        "/api/v1/jobs",
        headers=headers,
        json={
            "name": "Correlation Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code in {200, 201}

    returned_correlation_id = response.headers.get("X-Correlation-ID")

    assert returned_correlation_id == correlation_id
