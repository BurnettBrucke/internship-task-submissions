import json
import logging
import time
from datetime import datetime, timezone
from uuid import uuid4
from processing_service.app.queue import get_redis_pool
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from processing_service.app.core.security import verify_internal_service
from processing_service.app.database import get_db
from processing_service.app.models.job import Job
from processing_service.app.schemas.job import JobCreate, JobResponse

logger = logging.getLogger("processing.jobs")


def structured_log(
    *,
    level: str,
    event: str,
    job_id: str | None = None,
    correlation_id: str | None = None,
    duration_ms: float | None = None,
    status: str | None = None,
):
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": "processing-service",
        "event": event,
        "request_id": None,
        "correlation_id": correlation_id,
        "job_id": job_id,
        "duration_ms": None,
        "status": status,
    }

    logger.info(json.dumps(log_data))

router = APIRouter(
    prefix="/internal/v1/jobs",
    tags=["Internal Jobs"],
)


@router.post("", response_model=JobResponse, status_code=201)
async def create_job(
    payload: JobCreate,
    request: Request,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    _: bool = Depends(verify_internal_service),
    db: AsyncSession = Depends(get_db),
):
    start_time = time.perf_counter()


    existing_job = await db.execute(
       select(Job).where(Job.idempotency_key == idempotency_key)
    )

    existing = existing_job.scalar_one_or_none()

    if existing is not None:
        if (
           existing.name != payload.name
           or existing.job_type != payload.job_type
           or existing.priority != payload.priority
        ):

           raise HTTPException(
               status_code=409,
               detail="Idempotency key already used with a different payload",
            )

        return existing
    
    job = Job(
        job_id=str(uuid4()),
        name=payload.name,
        job_type=payload.job_type,
        priority=payload.priority,
        status="CREATED",
        idempotency_key=idempotency_key,
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)

    structured_log(
        level="INFO",
        event="job_created",
        job_id=job.job_id,
        correlation_id=request.state.correlation_id,
        duration_ms=round(
            (time.perf_counter() - start_time) * 1000,
             2,
        ),
        status=job.status,
    )
     
    redis = await get_redis_pool()

    await redis.enqueue_job(
    "process_job",
    job.job_id,
    )

    job.status = "QUEUED"
    await db.commit()

    await redis.aclose()

    return job

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    _: bool = Depends(verify_internal_service),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Job).where(Job.job_id == job_id)
    )

    job = result.scalar_one_or_none()

    if job is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job