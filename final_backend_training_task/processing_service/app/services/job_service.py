from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.schemas.job import JobCreate, JobStatus


async def create_job(
    session: AsyncSession,
    payload: JobCreate,
):
    job = Job(
        name=payload.name,
        job_type=payload.job_type,
        priority=payload.priority,
        status=JobStatus.CREATED,
    )

    session.add(job)

    await session.commit()
    await session.refresh(job)

    return job