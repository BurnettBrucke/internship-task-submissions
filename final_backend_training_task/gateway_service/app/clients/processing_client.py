import asyncio

import httpx
from fastapi import status

from app.core.config import settings
from app.core.errors import GatewayServiceError
from app.core.request_context import (
    get_correlation_id,
    get_request_id,
)
from app.schemas.job import JobCreate


class ProcessingClient:
    MAX_GET_ATTEMPTS = 2
    RETRY_DELAY_SECONDS = 0.2

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": (f"Bearer {settings.processing_service_token}"),
            "X-Request-ID": get_request_id() or "",
            "X-Correlation-ID": get_correlation_id() or "",
        }

    def _timeout(self) -> httpx.Timeout:
        return httpx.Timeout(
            timeout=settings.processing_timeout_seconds,
            connect=2.0,
        )

    def _map_response_error(
        self,
        response: httpx.Response,
    ) -> None:

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise GatewayServiceError(
                status_code=401,
                code="PROCESSING_AUTH_FAILED",
                message="Processing service rejected internal credentials",
            )

        if response.status_code == status.HTTP_403_FORBIDDEN:
            raise GatewayServiceError(
                status_code=403,
                code="PROCESSING_FORBIDDEN",
                message="Processing service denied the operation",
            )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise GatewayServiceError(
                status_code=404,
                code="JOB_NOT_FOUND",
                message="Job not found",
            )

        if response.status_code == status.HTTP_409_CONFLICT:
            raise GatewayServiceError(
                status_code=409,
                code="CONFLICT",
                message="Request conflicts with existing data",
            )

        if response.status_code >= 500:
            raise GatewayServiceError(
                status_code=503,
                code="PROCESSING_UNAVAILABLE",
                message="Processing service returned a server error",
            )

        if response.status_code >= 400:
            raise GatewayServiceError(
                status_code=502,
                code="PROCESSING_BAD_RESPONSE",
                message="Processing service returned an unexpected response",
            )

    async def create_job(
        self,
        payload: JobCreate,
    ) -> dict:

        try:
            async with httpx.AsyncClient(
                base_url=settings.processing_base_url,
                timeout=self._timeout(),
            ) as client:
                response = await client.post(
                    "/internal/v1/jobs",
                    json=payload.model_dump(mode="json"),
                    headers=self._headers(),
                )

        except httpx.ConnectTimeout as exc:
            raise GatewayServiceError(
                status_code=503,
                code="PROCESSING_UNAVAILABLE",
                message="Processing service is unavailable",
            ) from exc

        except httpx.ReadTimeout as exc:
            raise GatewayServiceError(
                status_code=504,
                code="PROCESSING_TIMEOUT",
                message="Processing service timed out",
            ) from exc

        except httpx.WriteTimeout as exc:
            raise GatewayServiceError(
                status_code=504,
                code="PROCESSING_TIMEOUT",
                message="Processing service timed out",
            ) from exc

        except httpx.PoolTimeout as exc:
            raise GatewayServiceError(
                status_code=503,
                code="PROCESSING_UNAVAILABLE",
                message="Processing service is unavailable",
            ) from exc

        except httpx.ConnectError as exc:
            raise GatewayServiceError(
                status_code=503,
                code="PROCESSING_UNAVAILABLE",
                message="Processing service is unavailable",
            ) from exc

        except httpx.RequestError as exc:
            raise GatewayServiceError(
                status_code=503,
                code="PROCESSING_UNAVAILABLE",
                message="Processing service is unavailable",
            ) from exc
        self._map_response_error(response)

        return response.json()

    async def get_job(
        self,
        job_id: int,
    ) -> dict:

        last_error: Exception | None = None

        for attempt in range(self.MAX_GET_ATTEMPTS):
            try:
                async with httpx.AsyncClient(
                    base_url=settings.processing_base_url,
                    timeout=self._timeout(),
                ) as client:
                    response = await client.get(
                        f"/internal/v1/jobs/{job_id}",
                        headers=self._headers(),
                    )

                # Retry only transient downstream errors.
                if (
                    response.status_code in {502, 503, 504}
                    and attempt < self.MAX_GET_ATTEMPTS - 1
                ):
                    await asyncio.sleep(self.RETRY_DELAY_SECONDS)
                    continue

                self._map_response_error(response)

                return response.json()

            except httpx.TimeoutException as exc:
                last_error = exc

                if attempt < self.MAX_GET_ATTEMPTS - 1:
                    await asyncio.sleep(self.RETRY_DELAY_SECONDS)
                    continue

                raise GatewayServiceError(
                    status_code=504,
                    code="PROCESSING_TIMEOUT",
                    message="Processing service timed out",
                ) from exc

            except httpx.RequestError as exc:
                last_error = exc

                if attempt < self.MAX_GET_ATTEMPTS - 1:
                    await asyncio.sleep(self.RETRY_DELAY_SECONDS)
                    continue

                raise GatewayServiceError(
                    status_code=503,
                    code="PROCESSING_UNAVAILABLE",
                    message="Processing service is unavailable",
                ) from exc

        raise GatewayServiceError(
            status_code=503,
            code="PROCESSING_UNAVAILABLE",
            message="Processing service is unavailable",
        ) from last_error
