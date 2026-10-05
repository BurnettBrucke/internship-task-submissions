from fastapi import APIRouter

from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import create_job


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
)
async def create_gateway_job(
    payload: JobCreate,
):
    return await create_job(payload)