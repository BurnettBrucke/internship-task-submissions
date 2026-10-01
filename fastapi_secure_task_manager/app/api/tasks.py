# ============================================================
# TASK API ROUTES
# ============================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import (
    create_task,
    get_all_tasks,
    get_task,
    update_task,
    delete_task,
)
from app.core.errors import (
    forbidden_error,
    not_found_error,
)


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
)


# ============================================================
# CREATE TASK
# ============================================================

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new task.

    The logged-in user becomes the owner.
    """

    username = current_user["sub"]

    return await create_task(
        db=db,
        task=task,
        owner_username=username,
    )


# ============================================================
# GET ALL TASKS
# ============================================================

@router.get("")
async def list_tasks(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get paginated tasks.

    Admin:
        Can see all tasks.

    Normal user:
        Can see only their own tasks.
    """

    role = current_user["role"]

    if role == "admin":
        return await get_all_tasks(
            db=db,
            owner_username=None,
            page=page,
            page_size=page_size,
        )

    username = current_user["sub"]

    return await get_all_tasks(
        db=db,
        owner_username=username,
        page=page,
        page_size=page_size,
    )


# ============================================================
# GET SINGLE TASK
# ============================================================

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_single_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get one task.

    Admin can access any task.
    Normal users can access only their own task.
    """

    task = await get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise not_found_error("Task not found")

    username = current_user["sub"]
    role = current_user["role"]

    if (
        role != "admin"
        and task["owner_username"] != username
    ):
        raise forbidden_error(
            "You do not have permission to access this task"
        )

    return task


# ============================================================
# UPDATE TASK
# ============================================================

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
    """
    Update a task.

    Admin can update any task.
    Normal users can update only their own task.

    Status changes are recorded in task_history.
    """

    task = await get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise not_found_error("Task not found")

    username = current_user["sub"]
    role = current_user["role"]

    if (
        role != "admin"
        and task["owner_username"] != username
    ):
        raise forbidden_error(
            "You do not have permission to update this task"
        )

    # Get database user ID for task history.
    from app.repositories.task_repository import (
        get_user_by_username,
    )

    user = await get_user_by_username(
        db,
        username=username,
    )

    if user is None:
        raise not_found_error("User not found")

    return await update_task(
        db=db,
        task_id=task_id,
        task=task_data,
        changed_by=user.id,
    )


# ============================================================
# DELETE TASK
# ============================================================

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_existing_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a task.

    Admin can delete any task.
    Normal users can delete only their own task.
    """

    task = await get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise not_found_error("Task not found")

    username = current_user["sub"]
    role = current_user["role"]

    if (
        role != "admin"
        and task["owner_username"] != username
    ):
        raise forbidden_error(
            "You do not have permission to delete this task"
        )

    await delete_task(
        db=db,
        task_id=task_id,
    )