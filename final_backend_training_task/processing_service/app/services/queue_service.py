from arq.jobs import Job
from opentelemetry import trace
from opentelemetry.propagate import inject

from app.core.arq import create_arq_pool

tracer = trace.get_tracer("day8.processing.queue")


async def enqueue_process_job(
    job_id: int,
    request_id: str | None,
    correlation_id: str | None,
) -> Job | None:

    redis = await create_arq_pool()

    try:
        with tracer.start_as_current_span("arq.enqueue") as span:
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

            # Capture the current OpenTelemetry
            # context so the worker can continue
            # the same trace later.
            trace_context: dict[str, str] = {}

            inject(trace_context)

            return await redis.enqueue_job(
                "process_job",
                job_id,
                request_id,
                correlation_id,
                trace_context,
                _job_id=f"process-job-{job_id}",
            )

    finally:
        await redis.close(close_connection_pool=True)
