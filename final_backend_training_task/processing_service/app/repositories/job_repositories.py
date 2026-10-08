from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job


class JobRepository:
    async def create(
        self,
        session: AsyncSession,
        job: Job,
    ) -> Job:
        session.add(job)

        await session.commit()
        await session.refresh(job)

        return job

    async def get_by_id(
        self,
        session: AsyncSession,
        job_id: int,
    ) -> Job | None:
        result = await session.execute(select(Job).where(Job.id == job_id))

        return result.scalar_one_or_none()
