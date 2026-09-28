from fastapi import APIRouter, Depends,status
from app.core.errors import AppException

from app.dependencies.auth import get_current_user
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.services import task_service


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


def check_task_permission(
    task: dict,
    current_user: dict
):
    if current_user["role"] == "admin":
        return

    if task["owner_id"] != current_user["id"]:
        raise AppException(
            status_code=403,
            code="FORBIDDEN",
            message="You do not have permission to access this task."
        )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user)
):
    return task_service.create_task(
        task_data,
        owner_id=current_user["id"]
    )


@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] == "admin":
        return task_service.get_tasks()

    return task_service.get_user_tasks(
        current_user["id"]
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user)
):
    task = task_service.get_task(task_id)

    if task is None:
       raise AppException(
            status_code=404,
            code="TASK_NOT_FOUND",
            message="Task does not exist."
     )

    check_task_permission(
        task,
        current_user
    )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user)
):
    task = task_service.get_task(task_id)

    if task is None:
      raise AppException(
            status_code=404,
            code="TASK_NOT_FOUND",
            message="Task does not exist."
        )

    check_task_permission(
        task,
        current_user
    )

    return task_service.update_task(
        task_id,
        task_data
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user)
):
    task = task_service.get_task(task_id)

    if task is None:
          raise AppException(
                status_code=404,
                code="TASK_NOT_FOUND",
                message="Task does not exist."
            )

    check_task_permission(
        task,
        current_user
    )

    task_service.delete_task(task_id)

    return None