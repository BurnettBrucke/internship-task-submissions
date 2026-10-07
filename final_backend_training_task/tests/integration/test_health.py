import pytest


@pytest.mark.asyncio
async def test_gateway_health(gateway_client):
    response = await gateway_client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data.get("status") in {"ok", "healthy"}


@pytest.mark.asyncio
async def test_processing_health(processing_client):
    response = await processing_client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data.get("status") in {"ok", "healthy"}
