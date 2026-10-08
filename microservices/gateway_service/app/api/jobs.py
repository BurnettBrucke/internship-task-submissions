from fastapi import APIRouter, Depends, Request
from fastapi import APIRouter, Depends, Request, Header
from app.clients.processing_client import create_job, get_job
from app.schemas.job import JobCreate, JobResponse
from app.core.security import verify_jwt

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)


@router.post("", response_model=JobResponse, status_code=201)
async def create_gateway_job(
    payload: JobCreate,
    request: Request,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    current_user: dict = Depends(verify_jwt),
):
    return await create_job(
        payload.model_dump(),
        request.state.correlation_id,
        idempotency_key,
    )

@router.get("/{job_id}", response_model=JobResponse)
async def get_gateway_job(
    job_id: str,
    request: Request,
    current_user: dict = Depends(verify_jwt),
):
    return await get_job(
        job_id,
        request.state.correlation_id,
    )