import asyncio
import json
import logging
import time
from datetime import datetime, timezone

from arq.connections import RedisSettings
from sqlalchemy import select

from processing_service.app.core.config import settings
from processing_service.app.database import AsyncSessionLocal
from processing_service.app.models.job import Job


logger = logging.getLogger("processing.worker")


def structured_log(
    *,
    level: str,
    event: str,
    job_id: str,
    duration_ms: float | None = None,
    status: str | None = None,
):
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": "processing-service",
        "event": event,
        "request_id": None,
        "correlation_id": None,
        "job_id": job_id,
        "duration_ms": duration_ms,
        "status": status,
    }

    logger.info(json.dumps(log_data))


async def process_job(ctx, job_id: str):
    start_time = time.perf_counter()

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Job).where(Job.job_id == job_id)
        )

        job = result.scalar_one_or_none()

        if job is None:
            structured_log(
                level="WARNING",
                event="job_not_found",
                job_id=job_id,
                status="FAILED",
            )
            return

        try:
            job.status = "PROCESSING"
            await db.commit()

            structured_log(
                level="INFO",
                event="job_processing_started",
                job_id=job_id,
                status="PROCESSING",
            )

            await asyncio.sleep(2)

            job.status = "COMPLETED"
            await db.commit()

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            structured_log(
                level="INFO",
                event="job_completed",
                job_id=job_id,
                duration_ms=duration_ms,
                status="COMPLETED",
            )

        except Exception:
            job.status = "FAILED"
            await db.commit()

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            structured_log(
                level="ERROR",
                event="job_failed",
                job_id=job_id,
                duration_ms=duration_ms,
                status="FAILED",
            )


class WorkerSettings:
    functions = [process_job]
    redis_settings = RedisSettings.from_dsn(settings.redis_url)