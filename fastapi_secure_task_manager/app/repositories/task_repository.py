# ============================================================
# TASK REPOSITORY
# ============================================================
# This layer is responsible ONLY for database operations.
#
# Flow:
# API Router
#     ↓
# Service Layer
#     ↓
# Repository Layer
#     ↓
# PostgreSQL
# ============================================================

from sqlalchemy import delete, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.task_history import TaskHistory
from app.models.user import User

# ============================================================
# CREATE TASK
# ============================================================

async def create_task(
    db: AsyncSession,
    *,
    user_id: int,
    title: str,
    description: str | None,
    priority: str,
    status: str = "pending",
) -> Task:
    """
    Create a new task in PostgreSQL.
    """

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        status=status,
    )

    db.add(task)

    # Flush sends INSERT to the database so that
    # task.id becomes available without committing yet.
    await db.flush()

    # Refresh gets the latest database state.
    await db.refresh(task)

    return task


# ============================================================
# GET TASK BY ID
# ============================================================

async def get_task_by_id(
    db: AsyncSession,
    *,
    task_id: int,
) -> Task | None:
    """
    Get one task by ID along with its owner.
    """

    result = await db.execute(
        select(Task)
        .options(selectinload(Task.owner))
        .where(Task.id == task_id)
    )

    return result.scalar_one_or_none()

# ============================================================
# GET ALL TASKS
# ============================================================

async def get_tasks(
    db: AsyncSession,
    *,
    user_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
) -> list[Task]:
    """
    Get tasks from PostgreSQL.

    If user_id is provided:
        Return only that user's tasks.

    If user_id is None:
        Return tasks for all users.
        This is useful for admin users.

    Pagination is performed directly in PostgreSQL
    using OFFSET and LIMIT.
    """

    query = select(Task).options(selectinload(Task.owner))

    if user_id is not None:
        query = query.where(Task.user_id == user_id)

    query = (
        query
        .order_by(Task.id)
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(query)

    return list(result.scalars().all())


# ============================================================
# COUNT TASKS
# ============================================================

async def count_tasks(
    db: AsyncSession,
    *,
    user_id: int | None = None,
) -> int:
    """
    Count tasks for pagination.

    If user_id is provided:
        Count only that user's tasks.

    If user_id is None:
        Count all tasks.
    """

    query = select(func.count(Task.id))

    if user_id is not None:
        query = query.where(Task.user_id == user_id)

    result = await db.execute(query)

    return result.scalar_one()


# ============================================================
# UPDATE TASK
# ============================================================

async def update_task(
    db: AsyncSession,
    *,
    task: Task,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    status: str | None = None,
) -> Task:
    """
    Update an existing task.

    Only values that are not None are updated.
    """

    if title is not None:
        task.title = title

    if description is not None:
        task.description = description

    if priority is not None:
        task.priority = priority

    if status is not None:
        task.status = status

    await db.flush()
    await db.refresh(task)

    return task


# ============================================================
# DELETE TASK
# ============================================================

async def delete_task(
    db: AsyncSession,
    *,
    task: Task,
) -> None:
    """
    Delete a task from PostgreSQL.
    """

    await db.delete(task)
    await db.flush()


# ============================================================
# CREATE TASK HISTORY
# ============================================================

async def create_task_history(
    db: AsyncSession,
    *,
    task_id: int,
    changed_by: int,
    old_status: str | None,
    new_status: str,
) -> TaskHistory:
    """
    Create a task status-change history record.

    This function does NOT commit the transaction.
    The service layer will control the transaction.
    """

    history = TaskHistory(
        task_id=task_id,
        changed_by=changed_by,
        old_status=old_status,
        new_status=new_status,
    )

    db.add(history)

    await db.flush()
    await db.refresh(history)

    return history


# ============================================================
# GET TASK HISTORY
# ============================================================

async def get_task_history(
    db: AsyncSession,
    *,
    task_id: int,
) -> list[TaskHistory]:
    """
    Get all history records for a task.
    """

    result = await db.execute(
        select(TaskHistory)
        .where(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.id)
    )

    return list(result.scalars().all())


# ============================================================
# DELETE TASK HISTORY
# ============================================================

async def delete_task_history(
    db: AsyncSession,
    *,
    task_id: int,
) -> None:
    """
    Delete history records associated with a task.

    Normally the Task model's cascade relationship
    handles this automatically when a task is deleted.
    This function is kept available for explicit use
    if required later.
    """

    await db.execute(
        delete(TaskHistory)
        .where(TaskHistory.task_id == task_id)
    )

# ============================================================
# GET USER BY USERNAME
# ============================================================

from app.models.user import User


async def get_user_by_username(
    db: AsyncSession,
    *,
    username: str,
) -> User | None:
    """
    Find a user by username.

    This is required to convert the Day 6
    owner_username into the PostgreSQL user_id.
    """

    result = await db.execute(
        select(User).where(User.username == username)
    )

    return result.scalar_one_or_none()