import asyncio

import httpx

from fastapi.responses import JSONResponse

from gateway_service.app.core.auth import create_service_token
from gateway_service.app.core.config import settings
from gateway_service.app.core.logger import log_event


class ProcessingClient:
    """Client used by Gateway to communicate with Processing Service."""

    def __init__(self):
        self.base_url = settings.processing_base_url
        self.timeout = settings.processing_timeout_seconds

    async def health_check(self):
        """Call Processing Service health endpoint."""

        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
        ) as client:
            response = await client.get("/health")

        response.raise_for_status()

        return response.json()

    async def create_job(
        self,
        name: str,
        job_type: str,
        priority: str,
        user_id: str,
        correlation_id: str,
        request_id: str,
    ):
        """Create a job in the Processing Service."""

        token = create_service_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Correlation-ID": correlation_id,
        }

        data = {
            "name": name,
            "job_type": job_type,
            "priority": priority,
            "user_id": user_id,
        }

        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            ) as client:
                response = await client.post(
                    "/internal/v1/jobs",
                    json=data,
                    headers=headers,
                )

            response.raise_for_status()

            job = response.json()

            log_event(
                event="job_created",
                request_id=request_id,
                correlation_id=correlation_id,
                job_id=job.get("id"),
                status=job.get("status"),
            )

            return job

        except httpx.TimeoutException:
            log_event(
                event="processing_service_timeout",
                level="ERROR",
                request_id=request_id,
                correlation_id=correlation_id,
                status="504",
            )

            return JSONResponse(
                status_code=504,
                content={
                    "error": {
                        "code": "PROCESSING_SERVICE_TIMEOUT",
                        "message": "Processing service did not respond in time.",
                        "request_id": request_id,
                    }
                },
            )

        except httpx.ConnectError:
            log_event(
                event="processing_service_unavailable",
                level="ERROR",
                request_id=request_id,
                correlation_id=correlation_id,
                status="502",
            )

            return JSONResponse(
                status_code=502,
                content={
                    "error": {
                        "code": "PROCESSING_SERVICE_UNAVAILABLE",
                        "message": "Processing service is unavailable.",
                        "request_id": request_id,
                    }
                },
            )

    async def get_job(
        self,
        job_id,
        correlation_id,
        request_id,
    ):
        """Get a job from the Processing Service."""

        token = create_service_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Correlation-ID": correlation_id,
        }

        # Retry only the safe GET request.
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(
                    base_url=self.base_url,
                    timeout=self.timeout,
                ) as client:
                    response = await client.get(
                        f"/internal/v1/jobs/{job_id}",
                        headers=headers,
                    )

                if response.status_code == 404:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "error": {
                                "code": "JOB_NOT_FOUND",
                                "message": "Job not found.",
                                "request_id": request_id,
                            }
                        },
                    )

                response.raise_for_status()

                job = response.json()

                log_event(
                    event="job_fetched",
                    request_id=request_id,
                    correlation_id=correlation_id,
                    job_id=str(job_id),
                    status=job.get("status"),
                )

                return job

            except httpx.ConnectError:
                if attempt < 2:
                    await asyncio.sleep(1)
                    continue

                log_event(
                    event="processing_service_unavailable",
                    level="ERROR",
                    request_id=request_id,
                    correlation_id=correlation_id,
                    status="502",
                )

                return JSONResponse(
                    status_code=502,
                    content={
                        "error": {
                            "code": "PROCESSING_SERVICE_UNAVAILABLE",
                            "message": "Processing service is unavailable.",
                            "request_id": request_id,
                        }
                    },
                )

            except httpx.TimeoutException:
                if attempt < 2:
                    await asyncio.sleep(1)
                    continue

                log_event(
                    event="processing_service_timeout",
                    level="ERROR",
                    request_id=request_id,
                    correlation_id=correlation_id,
                    status="504",
                )

                return JSONResponse(
                    status_code=504,
                    content={
                        "error": {
                            "code": "PROCESSING_SERVICE_TIMEOUT",
                            "message": "Processing service did not respond in time.",
                            "request_id": request_id,
                        }
                    },
                )


processing_client = ProcessingClient()