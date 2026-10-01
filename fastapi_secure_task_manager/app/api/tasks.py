from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.task import (
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
)
from app.services import task_service
from app.services import cache_service

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
)


def check_task_permission(
    task: dict,
    current_user: dict,
):
    if current_user["role"] == "admin":
        return

    if task["owner_id"] != current_user["id"]:
        raise AppException(
            status_code=403,
            code="FORBIDDEN",
            message="You do not have permission to access this task.",
        )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await task_service.create_task(
        db,
        task_data,
        owner_id=current_user["id"],
    )

    await db.commit()
    await cache_service.invalidate_tasks_cache(
        current_user["id"]
    )

    return task

@router.get("", response_model=TaskListResponse)
async def get_tasks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user["id"]

    # Admin sees all tasks.
    # Don't cache the global task list because tasks can be
    # changed by any user.
    if current_user["role"] == "admin":
        return await task_service.get_tasks(
            db,
            page=page,
            page_size=page_size,
        )

    cached_tasks = await cache_service.get_cached_tasks(
        user_id,
        page,
        page_size,
    )

    if cached_tasks is not None:
        return cached_tasks

    
    tasks = await task_service.get_user_tasks(
            db,
            user_id,
            page=page,
            page_size=page_size,
        )

    await cache_service.cache_tasks(
        user_id,
        page,
        page_size,
        tasks,
    )

    return tasks

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await task_service.get_task(
        db,
        task_id,
    )

    if task is None:
        raise AppException(
            status_code=404,
            code="TASK_NOT_FOUND",
            message="Task does not exist.",
        )

    check_task_permission(
        task,
        current_user,
    )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
  ):
    task = await task_service.get_task(
        db,
        task_id,
    )

    if task is None:
        raise AppException(
            status_code=404,
            code="TASK_NOT_FOUND",
            message="Task does not exist.",
        )

    check_task_permission(
        task,
        current_user,
    )

    updated_task = await task_service.update_task(
                db,
                task_id,
                task_data,
                changed_by=current_user["id"],
    )

    await db.commit()
    await cache_service.invalidate_tasks_cache(
        task["owner_id"]
    )

    return updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
 ):
    task = await task_service.get_task(
        db,
        task_id,
    )

    if task is None:
        raise AppException(
            status_code=404,
            code="TASK_NOT_FOUND",
            message="Task does not exist.",
        )

    check_task_permission(
        task,
        current_user,
    )

    await task_service.delete_task(
        db,
        task_id,
    )

    await db.commit()
    await cache_service.invalidate_tasks_cache(
        task["owner_id"]
    )

    return None