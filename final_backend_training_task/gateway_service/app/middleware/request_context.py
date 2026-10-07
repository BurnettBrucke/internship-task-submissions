import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.request_context import (
    correlation_id_ctx,
    request_id_ctx,
)

logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        request_id = request.headers.get("X-Request-ID")

        if not request_id:
            request_id = str(uuid4())

        correlation_id = request.headers.get("X-Correlation-ID")

        if not correlation_id:
            correlation_id = str(uuid4())

        request_token = request_id_ctx.set(request_id)
        correlation_token = correlation_id_ctx.set(correlation_id)

        started = time.perf_counter()

        try:
            response = await call_next(request)

            duration_ms = round(
                (time.perf_counter() - started) * 1000,
                2,
            )

            job_id = None

            last_part = request.url.path.rstrip("/").split("/")[-1]

            if last_part.isdigit():
                job_id = int(last_part)

            logger.info(
                "HTTP request completed",
                extra={
                    "service": "gateway-service",
                    "event": "http_request_completed",
                    "request_id": request_id,
                    "correlation_id": correlation_id,
                    "job_id": job_id,
                    "duration_ms": duration_ms,
                    "status": response.status_code,
                },
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Correlation-ID"] = correlation_id

            return response

        except Exception:
            duration_ms = round(
                (time.perf_counter() - started) * 1000,
                2,
            )

            logger.exception(
                "HTTP request failed",
                extra={
                    "service": "gateway-service",
                    "event": "http_request_failed",
                    "request_id": request_id,
                    "correlation_id": correlation_id,
                    "job_id": None,
                    "duration_ms": duration_ms,
                    "status": 500,
                },
            )

            raise

        finally:
            request_id_ctx.reset(request_token)
            correlation_id_ctx.reset(correlation_token)
