from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import verify_service_token
from app.db.session import get_session
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import create_job


router = APIRouter(
    prefix="/internal/v1/jobs",
    tags=["Internal Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    dependencies=[Depends(verify_service_token)],
)
async def create_internal_job(
    payload: JobCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_job(session, payload)