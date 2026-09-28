from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import (
    create_task,
    get_all_tasks,
    get_task,
    update_task,
    delete_task,
)
from app.dependencies.auth import get_current_user
from app.core.errors import (
    forbidden_error,
    not_found_error,
)


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
):
    username = current_user["sub"]

    return create_task(
        task=task,
        owner_username=username,
    )


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def list_tasks(
    current_user: dict = Depends(get_current_user),
):
    username = current_user["sub"]
    role = current_user["role"]

    if role == "admin":
        return get_all_tasks()

    return get_all_tasks(owner_username=username)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_single_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
):
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    username = current_user["sub"]
    role = current_user["role"]

    if role != "admin" and task["owner_username"] != username:
        raise forbidden_error(
            "You do not have permission to access this task"
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
    task = get_task(task_id)

    if task is None:
        raise not_found_error("Task not found")

    username = current_user["sub"]
    role = current_user["role"]

    if role != "admin" and task["owner_username"] != username:
        raise forbidden_error(
            "You do not have permission to update this task"
        )

    return update_task(
        task_id=task_id,
        task=task_data,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_existing_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
):
    task = get_task(task_id)

    if task is None:
        raise not_found_error("Task not found")

    username = current_user["sub"]
    role = current_user["role"]

    if role != "admin" and task["owner_username"] != username:
        raise forbidden_error(
            "You do not have permission to delete this task"
        )

    delete_task(task_id)