import pytest


@pytest.mark.asyncio
async def test_login(gateway_client, auth_token):
    assert auth_token
    assert isinstance(auth_token, str)


@pytest.mark.asyncio
async def test_jobs_require_authentication(gateway_client):
    response = await gateway_client.get("/api/v1/jobs/999999")

    assert response.status_code == 401
