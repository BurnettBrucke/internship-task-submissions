from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
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


@router.get("")
async def list_tasks(
    page: int = 1,
    page_size: int = 10,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be at least 1 and page_size must be between 1 and 100.",
        )

    offset = (page - 1) * page_size

    user_id = None

    if current_user["role"] != "admin":
        user_id = current_user["id"]

    return await get_tasks(
        db=db,
        user_id=user_id,
        offset=offset,
        limit=page_size,
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_task(
        db=db,
        user_id=current_user["id"],
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=task_data.status,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task_by_id(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await get_single_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist.",
        )

    if (
        current_user["role"] != "admin"
        and task.user_id != current_user["id"]
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
    db: AsyncSession = Depends(get_db),
):
    task = await get_single_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist.",
        )

    if (
        current_user["role"] != "admin"
        and task.user_id != current_user["id"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task.",
        )

    update_data = task_data.model_dump(
        exclude_unset=True,
    )

    return await update_task(
        db=db,
        task_id=task_id,
        changed_by=current_user["id"],
        data=update_data,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_existing_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await get_single_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist.",
        )

    if (
        current_user["role"] != "admin"
        and task.user_id != current_user["id"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task.",
        )

    await remove_task(
        db=db,
        task_id=task_id,
    )