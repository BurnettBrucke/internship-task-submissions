from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from processing_service.app.models.job import Job
from processing_service.app.repositories.job_repository import job_repository


class JobService:
    """Business logic for jobs."""

    async def create_job(
        self,
        session: AsyncSession,
        name: str,
        job_type: str,
        priority: str,
        user_id: UUID,
    ) -> Job:
        """Create a new job."""

        return await job_repository.create_job(
            session,
            name,
            job_type,
            priority,
            user_id,
        )

    async def get_job(
        self,
        session: AsyncSession,
        job_id,
    ) -> Job | None:
        """Get a job by its ID."""

        return await job_repository.get_job_by_id(
            session,
            job_id,
        )


job_service = JobService()