from enum import Enum

from pydantic import BaseModel, Field


class JobType(str, Enum):
    REPORT = "report"


class JobPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class JobStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    job_type: JobType
    priority: JobPriority


class JobResponse(BaseModel):
    id: int
    name: str
    job_type: JobType
    priority: JobPriority
    status: JobStatus
    