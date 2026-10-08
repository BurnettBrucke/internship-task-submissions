import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from processing_service.app.main import app
from processing_service.app.core.security import INTERNAL_SERVICE_TOKEN
from processing_service.app.database import engine , AsyncSessionLocal

from sqlalchemy import select
from processing_service.app.models.job import Job
from processing_service.app.worker import process_job

pytestmark = pytest.mark.asyncio(loop_scope="module")

@pytest.mark.asyncio
async def test_create_job_without_auth():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/internal/v1/jobs",
            json={
                "name": "Test Processing Job",
                "job_type": "email",
                "priority": "HIGH",
            },
            headers={
                "Idempotency-Key": "processing-test-001",
            },
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_job_with_valid_auth():
    await engine.dispose()
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/internal/v1/jobs",
            json={
                "name": "Test Processing Job",
                "job_type": "email",
                "priority": "HIGH",
            },
            headers={
                "Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}",
                "Idempotency-Key": "processing-test-002",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert "job_id" in data
    assert data["name"] == "Test Processing Job"
    assert data["job_type"] == "email"
    assert data["priority"] == "HIGH"

@pytest.mark.asyncio
async def test_create_job_idempotency():
    await engine.dispose()

    transport = ASGITransport(app=app)

    headers = {
        "Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}",
        "Idempotency-Key": "processing-idempotency-001",
    }

    payload = {
        "name": "Idempotency Test Job",
        "job_type": "email",
        "priority": "HIGH",
    }

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        first_response = await client.post(
            "/internal/v1/jobs",
            json=payload,
            headers=headers,
        )

        second_response = await client.post(
            "/internal/v1/jobs",
            json=payload,
            headers=headers,
        )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_job = first_response.json()
    second_job = second_response.json()

    assert first_job["job_id"] == second_job["job_id"]


@pytest.mark.asyncio
async def test_create_job_same_idempotency_key_different_payload():
    await engine.dispose()
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        headers = {
            "Authorization": "Bearer day8-internal-secret",
            "Idempotency-Key": "test-different-payload-001",
        }

        first_response = await client.post(
            "/internal/v1/jobs",
            json={
                "name": "First Job",
                "job_type": "report",
                "priority": "HIGH",
            },
            headers=headers,
        )

        assert first_response.status_code == 201

        second_response = await client.post(
            "/internal/v1/jobs",
            json={
                "name": "Different Job",
                "job_type": "report",
                "priority": "HIGH",
            },
            headers=headers,
        )

        assert second_response.status_code == 409
        assert (
            second_response.json()["detail"]
            == "Idempotency key already used with a different payload"
        )

@pytest.mark.asyncio
async def test_job_status_flow():
    await engine.dispose()

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        headers = {
            "Authorization": "Bearer day8-internal-secret",
            "Idempotency-Key": "status-flow-test-001",
        }

        response = await client.post(
            "/internal/v1/jobs",
            json={
                "name": "Status Flow Job",
                "job_type": "report",
                "priority": "HIGH",
            },
            headers=headers,
        )

        assert response.status_code == 201

        job_id = response.json()["job_id"]

        # Job should be queued or already completed
        # depending on whether the ARQ worker is running.
        assert response.json()["status"] in {
            "QUEUED",
            "COMPLETED",
        } 

        # If worker has not processed it yet, run it manually.
        if response.json()["status"] == "QUEUED":
            await process_job(None, job_id)

        # Verify final status
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Job).where(Job.job_id == job_id)
            )
            job = result.scalar_one()

        assert job.status == "COMPLETED"