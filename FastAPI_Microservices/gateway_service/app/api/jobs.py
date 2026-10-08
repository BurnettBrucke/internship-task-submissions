from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from gateway_service.app.clients.processing_client import processing_client
from gateway_service.app.core.auth import decode_user_token
from gateway_service.app.schemas.job import JobCreateRequest, JobResponse
from gateway_service.app.services.idempotency_service import idempotency_service


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job(
    request: JobCreateRequest,
    http_request: Request,
    idempotency_key: str | None = Header(default=None),
    current_user: dict = Depends(decode_user_token),
):
    """Create a new job through the Processing Service."""

    if idempotency_key:
        request_hash = idempotency_service.create_request_hash(
            name=request.name,
            job_type=request.job_type,
            priority=request.priority,
        )

        existing_result = await idempotency_service.get_result(
            idempotency_key
        )

        if existing_result:
            if existing_result["request_hash"] != request_hash:
                raise HTTPException(
                    status_code=409,
                    detail="Idempotency-Key already used with different payload",
                )

            return existing_result["response"]

        lock_acquired = await idempotency_service.acquire_lock(
            idempotency_key
        )

        if not lock_acquired:
            raise HTTPException(
                status_code=409,
                detail="Request with this Idempotency-Key is already in progress",
            )

    try:
        job = await processing_client.create_job(
            name=request.name,
            job_type=request.job_type,
            priority=request.priority,
            user_id=current_user["user_id"],
            correlation_id=http_request.state.correlation_id,
            request_id=http_request.state.request_id,
        )

        if idempotency_key:
            await idempotency_service.save_result(
                idempotency_key=idempotency_key,
                request_hash=request_hash,
                response_data=job,
            )

        return job

    finally:
        if idempotency_key:
            await idempotency_service.release_lock(
                idempotency_key
            )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
async def get_job(
    job_id: UUID,
    http_request: Request,
    current_user: dict = Depends(decode_user_token),
):
    """Get a job through the Processing Service."""

    job = await processing_client.get_job(
        job_id,
        http_request.state.correlation_id,
        http_request.state.request_id,
    )

    return job