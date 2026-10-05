import httpx

from app.core.config import settings
from app.schemas.job import JobCreate


class ProcessingClient:

    async def create_job(self, payload: JobCreate):

        headers = {
            "Authorization": (
                f"Bearer {settings.gateway_service_token}"
            )
        }

        async with httpx.AsyncClient(
            base_url=settings.processing_base_url,
            timeout=settings.processing_timeout_seconds,
        ) as client:

            response = await client.post(
                "/internal/v1/jobs",
                json=payload.model_dump(mode="json"),
                headers=headers,
            )

            response.raise_for_status()

            return response.json()