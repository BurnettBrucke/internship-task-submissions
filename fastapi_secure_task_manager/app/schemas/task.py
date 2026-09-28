from typing import Literal

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    priority: Literal["low", "medium", "high"]
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(
    default=None,
    min_length=3,
    max_length=100,
)
    description: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: Literal["low", "medium", "high"]
    completed: bool
    owner_id: int