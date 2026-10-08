from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.core.redis import redis
from app.dependencies.auth import get_current_user
from app.schemas.job import JobCreate, JobResponse
from app.services.idempotency_service import (
    create_fingerprint,
    get_record,
    release_key,
    reserve_key,
    save_result,
)
from app.services.job_service import create_job, get_job

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=JobResponse,
)
async def create_gateway_job(
    payload: JobCreate,
    idempotency_key: str | None = Header(
        default=None,
        alias="Idempotency-Key",
    ),
):

    # No idempotency key = normal request.
    if not idempotency_key:
        return await create_job(payload)

    payload_data = payload.model_dump(mode="json")
    fingerprint = create_fingerprint(payload_data)

    # Check existing request.
    existing = await get_record(
        redis,
        idempotency_key,
    )

    if existing is not None:
        # Same key, different payload.
        if existing["fingerprint"] != fingerprint:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=("Idempotency-Key was already used with a different payload."),
            )

        # Same key, completed request.
        if existing["state"] == "COMPLETED":
            return existing["job"]

        # Same key, request currently running.
        if existing["state"] == "IN_PROGRESS":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=("Request with this Idempotency-Key is already in progress."),
            )

    # Atomically reserve the key.
    owner = await reserve_key(
        redis,
        idempotency_key,
        fingerprint,
    )

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=("Request with this Idempotency-Key is already in progress."),
        )

    try:
        job = await create_job(payload)

        await save_result(
            redis,
            idempotency_key,
            fingerprint,
            job,
        )

        return job

    except Exception:
        await release_key(
            redis,
            idempotency_key,
            owner,
        )
        raise


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
async def get_gateway_job(
    job_id: int,
):
    return await get_job(job_id)
