import pytest


@pytest.mark.asyncio
async def test_invalid_service_token(processing_client):
    response = await processing_client.post(
        "/internal/v1/jobs",
        headers={
            "Authorization": "Bearer definitely-wrong-token",
        },
        json={
            "name": "Invalid Token Test",
            "job_type": "report",
            "priority": "medium",
        },
    )

    assert response.status_code == 401
