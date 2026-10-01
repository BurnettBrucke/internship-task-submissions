from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str | None = None

    priority: Literal["low", "medium", "high"]

    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        max_length=200
    )

    description: str | None = None

    priority: Literal["low", "medium", "high"] | None = None

    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: Literal["low", "medium", "high"]
    completed: bool
    owner_id: int


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    page: int
    page_size: int
    total: int