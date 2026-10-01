from typing import Literal

from pydantic import BaseModel, Field


TaskStatus = Literal["pending", "in_progress", "completed"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    priority: Literal["low", "medium", "high"] = "medium"
    status: TaskStatus = "pending"


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    status: TaskStatus | None = None


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    priority: Literal["low", "medium", "high"]
    status: TaskStatus

    model_config = {
        "from_attributes": True
    }