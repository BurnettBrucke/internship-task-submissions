import os
from urllib.parse import urlparse
from uuid import UUID

from arq.connections import RedisSettings
from sqlalchemy import select

from processing_service.app.core.database import AsyncSessionLocal
from processing_service.app.core.logger import log_event
from processing_service.app.models.job import Job, JobStatus


async def process_job(ctx, job_id: str):
    """Process a job in the background."""

    job_uuid = UUID(job_id)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Job).where(Job.id == job_uuid)
        )
        job = result.scalar_one_or_none()

        if job is None:
            log_event(
                event="job_not_found",
                level="ERROR",
                job_id=job_id,
            )
            return

        job.status = JobStatus.PROCESSING
        await session.commit()

        log_event(
            event="job_processing_started",
            job_id=job_id,
            status=JobStatus.PROCESSING.value,
        )

        try:
            # Actual background work will be added later.
            pass

            job.status = JobStatus.COMPLETED
            await session.commit()

            log_event(
                event="job_completed",
                job_id=job_id,
                status=JobStatus.COMPLETED.value,
            )

            return {
                "job_id": job_id,
                "status": JobStatus.COMPLETED.value,
            }

        except Exception:
            job.status = JobStatus.FAILED
            await session.commit()

            log_event(
                event="job_failed",
                level="ERROR",
                job_id=job_id,
                status=JobStatus.FAILED.value,
            )

            return {
                "job_id": job_id,
                "status": JobStatus.FAILED.value,
            }


def get_redis_settings() -> RedisSettings:
    """Build ARQ Redis settings from REDIS_URL."""

    redis_url = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0",
    )

    parsed_url = urlparse(redis_url)

    return RedisSettings(
        host=parsed_url.hostname or "localhost",
        port=parsed_url.port or 6379,
        database=int(parsed_url.path.lstrip("/") or 0),
    )


class WorkerSettings:
    functions = [process_job]
    redis_settings = get_redis_settings()