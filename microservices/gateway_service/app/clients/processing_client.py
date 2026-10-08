import asyncio
import json
import logging
import time
from datetime import datetime, timezone
import httpx
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger("gateway.client")


def structured_log(
    *,
    level: str,
    event: str,
    correlation_id: str,
    job_id: str | None = None,
    duration_ms: float | None = None,
    status: int | None = None,
):
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": "gateway-service",
        "event": event,
        "request_id": None,
        "correlation_id": correlation_id,
        "job_id": job_id,
        "duration_ms": duration_ms,
        "status": status,
    }

    logger.info(json.dumps(log_data))

async def create_job(
    payload: dict,
    correlation_id: str,
    idempotency_key: str,
):
    start_time = time.perf_counter()

    headers = {
        "Authorization": f"Bearer {settings.internal_service_token}",
        "X-Correlation-ID": correlation_id,
        "Idempotency-Key": idempotency_key,
    }

    try:
        async with httpx.AsyncClient(
            timeout=settings.processing_timeout_seconds
        ) as client:
            response = await client.post(
                f"{settings.processing_base_url}/internal/v1/jobs",
                json=payload,
                headers=headers,
            )

    except httpx.TimeoutException:
        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        structured_log(
            level="ERROR",
            event="processing_service_timeout",
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=504,
        )

        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Processing service timeout",
        )

    except httpx.RequestError:
        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        structured_log(
            level="ERROR",
            event="processing_service_unavailable",
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=503,
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Processing service unavailable",
        )

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2,
    )

    if response.status_code >= 500:
        structured_log(
            level="ERROR",
            event="processing_service_error",
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=503,
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Processing service unavailable",
        )

    if response.status_code == 401:
        structured_log(
            level="ERROR",
            event="processing_authentication_failed",
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=503,
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Processing service authentication failed",
        )

    if response.status_code == 404:
        structured_log(
            level="ERROR",
            event="processing_endpoint_unavailable",
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=503,
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Processing endpoint unavailable",
        )

    data = response.json()

    structured_log(
        level="INFO",
        event="job_created",
        correlation_id=correlation_id,
        job_id=data.get("job_id"),
        duration_ms=duration_ms,
        status=response.status_code,
    )

    return data

async def get_job(job_id: str, correlation_id: str):
    start_time = time.perf_counter()

    headers = {
        "Authorization": f"Bearer {settings.internal_service_token}",
        "X-Correlation-ID": correlation_id,
    }

    max_attempts = settings.processing_retry_count + 1

    for attempt in range(max_attempts):
        try:
            async with httpx.AsyncClient(
                timeout=settings.processing_timeout_seconds
            ) as client:
                response = await client.get(
                    f"{settings.processing_base_url}/internal/v1/jobs/{job_id}",
                    headers=headers,
                )

            # Successful response or normal application response
            if response.status_code < 500:
                break

            # 5xx response → retry if attempts remain
            if attempt < max_attempts - 1:
                await asyncio.sleep(
                    settings.processing_retry_delay_seconds
                )
                continue

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            structured_log(
                level="ERROR",
                event="processing_service_error",
                correlation_id=correlation_id,
                job_id=job_id,
                duration_ms=duration_ms,
                status=503,
            )

            raise HTTPException(
                status_code=503,
                detail="Processing service unavailable",
            )

        except httpx.TimeoutException:
            if attempt < max_attempts - 1:
                await asyncio.sleep(
                    settings.processing_retry_delay_seconds
                )
                continue

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            structured_log(
                level="ERROR",
                event="processing_service_timeout",
                correlation_id=correlation_id,
                job_id=job_id,
                duration_ms=duration_ms,
                status=504,
            )

            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Processing service timeout",
            )

        except httpx.RequestError:
            if attempt < max_attempts - 1:
                await asyncio.sleep(
                    settings.processing_retry_delay_seconds
                )
                continue

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            structured_log(
                level="ERROR",
                event="processing_service_unavailable",
                correlation_id=correlation_id,
                job_id=job_id,
                duration_ms=duration_ms,
                status=503,
            )

            raise HTTPException(
                status_code=503,
                detail="Processing service unavailable",
            )

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2,
    )

    if response.status_code == 404:
        structured_log(
            level="WARNING",
            event="job_not_found",
            correlation_id=correlation_id,
            job_id=job_id,
            duration_ms=duration_ms,
            status=404,
        )

        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    data = response.json()

    structured_log(
        level="INFO",
        event="job_fetched",
        correlation_id=correlation_id,
        job_id=job_id,
        duration_ms=duration_ms,
        status=response.status_code,
    )

    return data