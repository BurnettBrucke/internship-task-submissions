from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from processing_service.app.core.arq import get_arq_pool
from processing_service.app.core.auth import verify_service_token
from processing_service.app.core.database import get_db_session
from processing_service.app.core.logger import log_event
from processing_service.app.models.job import JobStatus
from processing_service.app.schemas.job import JobCreateRequest, JobResponse
from processing_service.app.services.job_service import job_service


router = APIRouter(
    prefix="/internal/v1/jobs",
    tags=["Jobs"],
    dependencies=[Depends(verify_service_token)],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job(
    request: JobCreateRequest,
    http_request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    correlation_id = http_request.headers.get("X-Correlation-ID")

    log_event(
        event="job_request_received",
        request_id=http_request.state.request_id,
        correlation_id=correlation_id,
    )

    """Create a new job."""

    job = await job_service.create_job(
        session,
        request.name,
        request.job_type,
        request.priority,
        request.user_id,
    )

    log_event(
        event="job_created",
        request_id=http_request.state.request_id,
        correlation_id=correlation_id,
        job_id=str(job.id),
        status=JobStatus.CREATED.value,
    )

    # Connect to ARQ
    pool = await get_arq_pool()

    # Add the job to Redis queue
    await pool.enqueue_job(
        "process_job",
        str(job.id),
        _job_id=str(job.id),
    )

    log_event(
        event="job_queued",
        request_id=http_request.state.request_id,
        correlation_id=correlation_id,
        job_id=str(job.id),
        status=JobStatus.QUEUED.value,
    )

    # Change status from CREATED to QUEUED
    job.status = JobStatus.QUEUED

    await session.commit()
    await session.refresh(job)

    log_event(
        event="job_status_updated",
        request_id=http_request.state.request_id,
        correlation_id=correlation_id,
        job_id=str(job.id),
        status=job.status.value,
    )

    # Close ARQ connection
    await pool.close()

    return job


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
async def get_job(
    job_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    """Get a job by its ID."""

    job = await job_service.get_job(
        session,
        job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job