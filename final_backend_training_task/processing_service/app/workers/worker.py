import asyncio
import logging
from typing import ClassVar

from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.trace import Status, StatusCode

from app.core.arq import get_redis_settings
from app.core.logging_config import configure_logging
from app.core.telemetry import configure_tracing
from app.db.session import AsyncSessionLocal
from app.models.job import Job
from app.schemas.job import JobStatus

configure_tracing()

tracer = trace.get_tracer("day8.processing.worker")

configure_logging()

logger = logging.getLogger(__name__)


async def process_job(
    ctx,
    job_id: int,
    request_id: str | None = None,
    correlation_id: str | None = None,
    trace_context: dict[str, str] | None = None,
):
    # Restore the trace context captured when the job
    # was added to the ARQ queue.
    parent_context = extract(trace_context or {})

    started = asyncio.get_running_loop().time()

    with tracer.start_as_current_span(
        "arq.worker.process_job",
        context=parent_context,
    ) as span:
        span.set_attribute(
            "job.id",
            job_id,
        )

        span.set_attribute(
            "job.type",
            "process_job",
        )

        if request_id:
            span.set_attribute(
                "request.id",
                request_id,
            )

        if correlation_id:
            span.set_attribute(
                "correlation.id",
                correlation_id,
            )

        try:
            logger.info(
                "Job processing started",
                extra={
                    "service": "processing-worker",
                    "event": "job_processing_started",
                    "request_id": request_id,
                    "correlation_id": correlation_id,
                    "job_id": job_id,
                    "duration_ms": None,
                    "status": "PROCESSING",
                },
            )

            async with AsyncSessionLocal() as session:
                job = await session.get(
                    Job,
                    job_id,
                )

                if job is None:
                    span.set_attribute(
                        "job.status",
                        "FAILED",
                    )

                    span.set_status(
                        Status(
                            StatusCode.ERROR,
                            "Job not found",
                        )
                    )

                    logger.error(
                        "Job not found",
                        extra={
                            "service": "processing-worker",
                            "event": "job_not_found",
                            "request_id": request_id,
                            "correlation_id": correlation_id,
                            "job_id": job_id,
                            "duration_ms": None,
                            "status": "FAILED",
                        },
                    )

                    return

                # Mark job as PROCESSING.
                job.status = JobStatus.PROCESSING

                await session.commit()

                span.set_attribute(
                    "job.status",
                    "PROCESSING",
                )

                # Simulated background work.
                await asyncio.sleep(2)

                # Mark job as COMPLETED.
                job.status = JobStatus.COMPLETED

                await session.commit()

                span.set_attribute(
                    "job.status",
                    "COMPLETED",
                )

                duration_ms = round(
                    (asyncio.get_running_loop().time() - started) * 1000,
                    2,
                )

                span.set_attribute(
                    "job.duration_ms",
                    duration_ms,
                )

                logger.info(
                    "Job completed",
                    extra={
                        "service": "processing-worker",
                        "event": "job_completed",
                        "request_id": request_id,
                        "correlation_id": correlation_id,
                        "job_id": job_id,
                        "duration_ms": duration_ms,
                        "status": "COMPLETED",
                    },
                )

        except Exception as exc:
            span.set_attribute(
                "job.status",
                "FAILED",
            )

            span.record_exception(exc)

            span.set_status(
                Status(
                    StatusCode.ERROR,
                    str(exc),
                )
            )

            duration_ms = round(
                (asyncio.get_running_loop().time() - started) * 1000,
                2,
            )

            logger.exception(
                "Job failed",
                extra={
                    "service": "processing-worker",
                    "event": "job_failed",
                    "request_id": request_id,
                    "correlation_id": correlation_id,
                    "job_id": job_id,
                    "duration_ms": duration_ms,
                    "status": "FAILED",
                },
            )

            # Try to persist FAILED state.
            try:
                async with AsyncSessionLocal() as session:
                    job = await session.get(
                        Job,
                        job_id,
                    )

                    if job is not None:
                        job.status = JobStatus.FAILED
                        await session.commit()

            except Exception:
                logger.exception(
                    "Failed to persist FAILED job status",
                    extra={
                        "service": "processing-worker",
                        "event": "job_failed_status_persist_error",
                        "request_id": request_id,
                        "correlation_id": correlation_id,
                        "job_id": job_id,
                        "duration_ms": duration_ms,
                        "status": "FAILED",
                    },
                )

            raise


class WorkerSettings:
    functions: ClassVar = [process_job]
    redis_settings = get_redis_settings()

    max_jobs = 10
    job_timeout = 300
    keep_result = 3600
