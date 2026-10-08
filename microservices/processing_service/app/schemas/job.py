from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    name: str = Field(min_length=1)
    job_type: str
    priority: str


class JobResponse(BaseModel):
    job_id: str
    name: str
    job_type: str
    priority: str
    status: str