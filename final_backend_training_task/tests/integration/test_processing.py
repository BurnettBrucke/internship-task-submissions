import uuid

import pytest

from tests.conftest import test_settings


@pytest.mark.asyncio
async def test_processing_receives_internal_job(processing_client):
    token = test_settings.processing_service_token

    if not token:
        pytest.fail(
            "PROCESSING_SERVICE_TOKEN is not available in the test environment."
        )

    response = await processing_client.post(
        "/internal/v1/jobs",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Request-ID": str(uuid.uuid4()),
            "X-Correlation-ID": str(uuid.uuid4()),
        },
        json={
            "name": "Processing Direct Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code in {200, 201}

    data = response.json()

    assert "id" in data
    assert data["name"] == "Processing Direct Test"
    assert data["status"] in {
        "CREATED",
        "QUEUED",
    }
