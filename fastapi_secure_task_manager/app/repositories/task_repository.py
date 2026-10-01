from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


async def create_task(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str | None,
    priority: str,
    status: str,
):
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        status=status,
    )

    db.add(task)
    await db.flush()

    return task


async def get_tasks(
    db: AsyncSession,
    user_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = select(Task).order_by(Task.id)

    if user_id is not None:
        query = query.where(Task.user_id == user_id)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


async def count_tasks(
    db: AsyncSession,
    user_id: int | None = None,
):
    query = select(func.count()).select_from(Task)

    if user_id is not None:
        query = query.where(Task.user_id == user_id)

    result = await db.execute(query)

    return result.scalar_one()


async def get_task_by_id(
    db: AsyncSession,
    task_id: int,
):
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )

    return result.scalar_one_or_none()


async def update_task(
    db: AsyncSession,
    task: Task,
    data: dict,
):
    for field, value in data.items():
        setattr(task, field, value)

    await db.flush()

    return task


async def delete_task(
    db: AsyncSession,
    task: Task,
):
    await db.delete(task)
    await db.flush()