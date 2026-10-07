from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.repositories.job_repositories import JobRepository
from app.schemas.job import JobCreate, JobStatus
from app.services.queue_service import enqueue_process_job

import logging

from app.core.request_context import (
    get_correlation_id,
    get_request_id,
)

logger = logging.getLogger(__name__)
job_repository = JobRepository()


async def create_job(
    session: AsyncSession,
    payload: JobCreate,
):
    job = Job(
        name=payload.name,
        job_type=payload.job_type,
        priority=payload.priority,
        status=JobStatus.CREATED,
    )

    session.add(job)

    # Get the database-generated ID.
    await session.flush()

    # Queue state is committed before the worker can consume the job.
    job.status = JobStatus.QUEUED

    await session.commit()
    await session.refresh(job)

    try:
        await enqueue_process_job(
            job.id,
            get_request_id(),
            get_correlation_id(),)

    except Exception as exc:
        job.status = JobStatus.FAILED

        await session.commit()

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to queue job",
        ) from exc

    return job


async def get_job(
    session: AsyncSession,
    job_id: int,
):
    job = await job_repository.get_by_id(
        session,
        job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job