from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.task import (
    TaskCreate,
    TaskListResponse,
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
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_task(
    data: TaskCreate,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task = await create_task(
        session=session,
        title=data.title,
        description=data.description,
        priority=data.priority,
        status=data.status,
        owner_id=current_user.id,
    )

    return task


@router.get(
    "",
    response_model=TaskListResponse,
)
async def list_tasks(
    search: str | None = None,
    priority: str | None = Query(
        default=None,
        pattern="^(low|medium|high)$",
    ),
    status_filter: str | None = Query(
        default=None,
        alias="status",
        pattern="^(pending|in_progress|completed)$",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await get_all_tasks(
        session=session,
        current_user=current_user,
        search=search,
        priority=priority,
        status=status_filter,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task, error = await get_task_by_id(
        session=session,
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
async def update_existing_task(
    task_id: int,
    data: TaskUpdate,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task, error = await update_task(
        session=session,
        task_id=task_id,
        current_user=current_user,
        title=data.title,
        description=data.description,
        priority=data.priority,
        status=data.status,
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
async def remove_task(
    task_id: int,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    _, error = await delete_task(
        session=session,
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