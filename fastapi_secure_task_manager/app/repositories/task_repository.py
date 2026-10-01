from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


async def create_task(
    db: AsyncSession,
    title: str,
    description: str | None,
    priority: str,
    completed: bool,
    owner_username: str,
):
    task = Task(
        title=title,
        description=description,
        priority=priority,
        completed=completed,
        owner_username=owner_username,
    )

    db.add(task)
    await db.flush()

    return task



async def get_all_tasks(
    db: AsyncSession,
    owner_username: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = select(Task).order_by(Task.id)

    if owner_username is not None:
        query = query.where(Task.owner_username == owner_username)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


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