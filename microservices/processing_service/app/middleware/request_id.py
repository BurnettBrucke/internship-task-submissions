import json
import logging
import time
from datetime import datetime, timezone
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


logger = logging.getLogger("processing")


def structured_log(
    *,
    level: str,
    event: str,
    request_id: str | None = None,
    correlation_id: str | None = None,
    job_id: str | None = None,
    duration_ms: float | None = None,
    status: int | None = None,
):
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": "processing-service",
        "event": event,
        "request_id": request_id,
        "correlation_id": correlation_id,
        "job_id": job_id,
        "duration_ms": duration_ms,
        "status": status,
    }

    logger.info(json.dumps(log_data))


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        correlation_id = request.headers.get("X-Correlation-ID")

        if not correlation_id:
            correlation_id = str(uuid4())

        request_id = str(uuid4())

        request.state.correlation_id = correlation_id
        request.state.request_id = request_id

        response = await call_next(request)

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        structured_log(
            level="INFO",
            event="request_completed",
            request_id=request_id,
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=response.status_code,
        )

        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Request-ID"] = request_id

        return response