from uuid import UUID

from pydantic import BaseModel


class JobCreateRequest(BaseModel):
    name: str
    job_type: str
    priority: str


class JobResponse(BaseModel):
    id: UUID
    status: str
    