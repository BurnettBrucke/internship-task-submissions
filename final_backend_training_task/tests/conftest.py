from pathlib import Path

import httpx
import pytest_asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class TestSettings(BaseSettings):
    jwt_demo_username: str
    jwt_demo_password: str
    processing_service_token: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


test_settings = TestSettings()  # type: ignore


GATEWAY_URL = "http://127.0.0.1:8000"
PROCESSING_URL = "http://127.0.0.1:8001"


@pytest_asyncio.fixture
async def gateway_client():
    async with httpx.AsyncClient(
        base_url=GATEWAY_URL,
        timeout=10.0,
    ) as client:
        yield client


@pytest_asyncio.fixture
async def processing_client():
    async with httpx.AsyncClient(
        base_url=PROCESSING_URL,
        timeout=10.0,
    ) as client:
        yield client


@pytest_asyncio.fixture
async def auth_token(gateway_client):
    response = await gateway_client.post(
        "/api/v1/auth/login",
        json={
            "username": test_settings.jwt_demo_username,
            "password": test_settings.jwt_demo_password,
        },
    )

    assert response.status_code == 200, (
        f"Login failed: {response.status_code} {response.text}"
    )

    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}",
    }
