from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from processing_service.app.models.job import Job, JobStatus


class JobRepository:
    """Database operations for jobs."""

    async def create_job(
        self,
        session: AsyncSession,
        name: str,
        job_type: str,
        priority: str,
        user_id: UUID,
    ) -> Job:
        """Create a new job in the database."""

        job = Job(
            user_id=user_id,
            name=name,
            job_type=job_type,
            priority=priority,
            status=JobStatus.CREATED,
        )

        session.add(job)

        await session.commit()
        await session.refresh(job)

        return job

    async def get_job_by_id(
        self,
        session: AsyncSession,
        job_id: UUID,
    ) -> Job | None:
        """Get a job by its ID."""

        result = await session.execute(
            select(Job).where(Job.id == job_id)
        )

        return result.scalar_one_or_none()


job_repository = JobRepository()