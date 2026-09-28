from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task,
    get_single_task,
    get_tasks,
    remove_task,
    update_task,
)

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
)


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def list_tasks(current_user: dict = Depends(get_current_user)):
    tasks = get_tasks()

    if current_user["role"] == "admin":
        return tasks

    return [
        task
        for task in tasks
        if task["owner_username"] == current_user["username"]
    ]


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
):
    return create_task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        completed=task_data.completed,
        owner_username=current_user["username"],
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task_by_id(
    task_id: int,
    current_user: dict = Depends(get_current_user),
):
    task = get_single_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist.",
        )

    if (
        current_user["role"] != "admin"
        and task["owner_username"] != current_user["username"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this task.",
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
):
    task = get_single_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist.",
        )

    if (
        current_user["role"] != "admin"
        and task["owner_username"] != current_user["username"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task.",
        )

    update_data = task_data.model_dump(exclude_unset=True)

    return update_task(task_id, update_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_existing_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
):
    task = get_single_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist.",
        )

    if (
        current_user["role"] != "admin"
        and task["owner_username"] != current_user["username"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task.",
        )

    remove_task(task_id)