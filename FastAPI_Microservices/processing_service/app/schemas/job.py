from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from processing_service.app.models.job import JobStatus


class JobCreateRequest(BaseModel):
    """Data received when a new job is created."""

    name: str
    job_type: str
    priority: str
    user_id: UUID


class JobResponse(BaseModel):
    """Data returned for a job."""

    id: UUID
    status: JobStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }