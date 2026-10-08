from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


async def create_task(
    db: AsyncSession,
    *,
    user_id: int,
    title: str,
    description: str | None,
    priority: str,
    status: str,
) -> Task:
    """
    Create a task in PostgreSQL.

    The repository only handles database operations.
    Business rules stay in the service layer.
    """

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        status=status,
    )

    db.add(task)

    # Send INSERT to PostgreSQL without committing yet.
    await db.flush()

    # Load generated values such as id and timestamps.
    await db.refresh(task)

    return task


async def get_task_by_id(
    db: AsyncSession,
    task_id: int,
) -> Task | None:
    """
    Retrieve one task by its primary key.
    """

    result = await db.execute(
        select(Task).where(
            Task.id == task_id
        )
    )

    return result.scalar_one_or_none()


async def get_tasks(
    db: AsyncSession,
    *,
    offset: int = 0,
    limit: int = 100,
) -> list[Task]:
    """
    Retrieve tasks with database-level pagination.
    """

    result = await db.execute(
        select(Task)
        .order_by(Task.id)
        .offset(offset)
        .limit(limit)
    )

    return list(result.scalars().all())


async def get_user_tasks(
    db: AsyncSession,
    *,
    user_id: int,
    offset: int = 0,
    limit: int = 100,
) -> list[Task]:
    """
    Retrieve only tasks belonging to one user.

    Pagination happens inside PostgreSQL using OFFSET/LIMIT.
    """

    result = await db.execute(
        select(Task)
        .where(
            Task.user_id == user_id
        )
        .order_by(Task.id)
        .offset(offset)
        .limit(limit)
    )

    return list(result.scalars().all())


async def count_tasks(
    db: AsyncSession,
) -> int:
    """
    Count all tasks.
    """

    result = await db.execute(
        select(func.count(Task.id))
    )

    return result.scalar_one()


async def count_user_tasks(
    db: AsyncSession,
    *,
    user_id: int,
) -> int:
    """
    Count tasks belonging to one user.
    """

    result = await db.execute(
        select(func.count(Task.id))
        .where(
            Task.user_id == user_id
        )
    )

    return result.scalar_one()


async def update_task(
    db: AsyncSession,
    task: Task,
    *,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    status: str | None = None,
) -> Task:
    """
    Update an existing task.

    Only values explicitly supplied by the service are changed.
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


async def delete_task(
    db: AsyncSession,
    task: Task,
) -> None:
    """
    Delete a task from PostgreSQL.
    """

    await db.delete(task)
    await db.flush()