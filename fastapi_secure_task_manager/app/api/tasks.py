from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies.auth import get_current_user
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.services.task_service import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_task(
    data: TaskCreate,
    current_user=Depends(get_current_user),
):
    task = create_task(
        title=data.title,
        description=data.description,
        priority=data.priority,
        completed=data.completed,
        owner_id=current_user["id"],
    )

    return task


@router.get(
    "",
    response_model=list[TaskResponse],
)
def list_tasks(
    search: str | None = None,
    priority: Literal["low", "medium", "high"] | None = None,
    completed: bool | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    sort_by: Literal["title", "priority", "completed"] | None = None,
    current_user=Depends(get_current_user),
):
    return get_all_tasks(
        current_user=current_user,
        search=search,
        priority=priority,
        completed=completed,
        sort_by=sort_by,
        page=page,
        limit=limit,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    current_user=Depends(get_current_user),
):
    task, error = get_task_by_id(
        task_id=task_id,
        current_user=current_user,
    )

    if error == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if error == "forbidden":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this task.",
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_existing_task(
    task_id: int,
    data: TaskUpdate,
    current_user=Depends(get_current_user),
):
    task, error = update_task(
        task_id=task_id,
        current_user=current_user,
        title=data.title,
        description=data.description,
        priority=data.priority,
        completed=data.completed,
    )

    if error == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if error == "forbidden":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this task.",
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_task(
    task_id: int,
    current_user=Depends(get_current_user),
):
    task, error = delete_task(
        task_id=task_id,
        current_user=current_user,
    )

    if error == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if error == "forbidden":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this task.",
        )

    return None