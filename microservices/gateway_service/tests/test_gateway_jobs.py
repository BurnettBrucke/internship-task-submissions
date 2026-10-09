import sys
import httpx
import pytest
from pathlib import Path
from uuid import uuid4
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.clients.processing_client import get_job
import pytest
from httpx import ASGITransport, AsyncClient
from app.database import engine
from app.main import app

pytestmark = pytest.mark.asyncio(loop_scope="module")

@pytest.mark.asyncio
async def test_create_job_without_jwt():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/api/v1/jobs",
            json={
                "name": "Test Job",
                "job_type": "email",
                "priority": "HIGH",
            },
            headers={
                "Idempotency-Key": "test-no-jwt-001",
            },
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_job_without_jwt():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/api/v1/jobs/non-existing-job",
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_job_with_invalid_jwt():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/api/v1/jobs",
            json={
                "name": "Test Job",
                "job_type": "email",
                "priority": "HIGH",
            },
            headers={
                "Authorization": "Bearer invalid-token",
                "Idempotency-Key": "test-invalid-jwt-001",
            },
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_job_with_valid_jwt():
    await engine.dispose()
    username = f"integration_user_{uuid4().hex[:8]}"
    password = "TestPassword123"

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        # Register
        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": password,
            },
        )

        assert register_response.status_code == 201

        # Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        # Create job through Gateway
        job_response = await client.post(
            "/api/v1/jobs",
            json={
                "name": "Integration Test Job",
                "job_type": "email",
                "priority": "HIGH",
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Idempotency-Key": "integration-job-002",
            },
        )

    assert job_response.status_code == 201

    data = job_response.json()

    assert data["name"] == "Integration Test Job"
    assert data["job_type"] == "email"
    assert data["priority"] == "HIGH"
    assert "job_id" in data

@pytest.mark.asyncio
async def test_create_job_invalid_payload():
    await engine.dispose()

    username = f"validation_user_{uuid4().hex[:8]}"

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": "TestPassword123",
            },
        )

        assert register_response.status_code == 201

        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": username,
                "password": "TestPassword123",
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        response = await client.post(
            "/api/v1/jobs",
            json={
                "name": "",
                "job_type": "",
                "priority": "",
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Idempotency-Key": "validation-test-001",
            },
        )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_job_not_found():
    await engine.dispose()

    username = f"not_found_user_{uuid4().hex[:8]}"
    password = "TestPassword123"

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        # Register
        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": password,
            },
        )

        assert register_response.status_code == 201

        # Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        # Request non-existing job
        response = await client.get(
            "/api/v1/jobs/non-existing-job-404",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"

@pytest.mark.asyncio
async def test_create_job_processing_service_unavailable():
    await engine.dispose()

    username = f"service_unavailable_{uuid4().hex[:8]}"
    password = "TestPassword123"

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        # Register
        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": password,
            },
        )

        assert register_response.status_code == 201

        # Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        # Mock only the AsyncClient used by Processing Client
        from unittest.mock import patch
        import httpx

        class MockProcessingClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

            async def post(self, *args, **kwargs):
                raise httpx.RequestError(
                    "Processing unavailable"
                )

        with patch(
            "app.clients.processing_client.httpx.AsyncClient",
            return_value=MockProcessingClient(),
        ):
            response = await client.post(
                "/api/v1/jobs",
                json={
                    "name": "Unavailable Test Job",
                    "job_type": "email",
                    "priority": "HIGH",
                },
                headers={
                    "Authorization": f"Bearer {token}",
                    "Idempotency-Key": f"unavailable-{uuid4().hex}",
                },
            )

    assert response.status_code == 503
    assert response.json()["detail"] == "Processing service unavailable"

@pytest.mark.asyncio
async def test_create_job_processing_service_timeout():
    await engine.dispose()

    username = f"timeout_user_{uuid4().hex[:8]}"
    password = "TestPassword123"

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        # Register
        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": password,
            },
        )

        assert register_response.status_code == 201

        # Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        from unittest.mock import patch
        import httpx

        class MockProcessingClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

            async def post(self, *args, **kwargs):
                raise httpx.ReadTimeout(
                    "Processing service timeout"
                )

        with patch(
            "app.clients.processing_client.httpx.AsyncClient",
            return_value=MockProcessingClient(),
        ):
            response = await client.post(
                "/api/v1/jobs",
                json={
                    "name": "Timeout Test Job",
                    "job_type": "email",
                    "priority": "HIGH",
                },
                headers={
                    "Authorization": f"Bearer {token}",
                    "Idempotency-Key": f"timeout-{uuid4().hex}",
                },
            )

    assert response.status_code == 504
    assert response.json()["detail"] == "Processing service timeout"

@pytest.mark.asyncio
async def test_gateway_request_and_correlation_ids():
    transport = ASGITransport(app=app)

    correlation_id = str(uuid4())

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        response = await client.get(
            "/health",
            headers={
                "X-Correlation-ID": correlation_id,
            },
        )

    assert response.status_code == 200

    assert response.headers["X-Correlation-ID"] == correlation_id
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]

@pytest.mark.asyncio
async def test_get_job_retries_on_processing_failure(monkeypatch):
    attempts = 0

    class MockResponse:
        status_code = 200

        def json(self):
            return {
                "job_id": "retry-test-job",
                "name": "Retry Test Job",
                "job_type": "email",
                "priority": "HIGH",
                "status": "COMPLETED",
            }

    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, *args, **kwargs):
            nonlocal attempts
            attempts += 1

            if attempts < 3:
                raise httpx.RequestError("Temporary failure")

            return MockResponse()

    monkeypatch.setattr(
        "app.clients.processing_client.httpx.AsyncClient",
        lambda *args, **kwargs: MockClient(),
    )

    result = await get_job(
        "retry-test-job",
        "test-correlation-id",
    )

    assert result["job_id"] == "retry-test-job"
    assert attempts == 3