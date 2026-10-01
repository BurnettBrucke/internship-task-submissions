from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_history_repository import create_task_history
from app.services.cache_service import get_cache, set_cache, invalidate_task_cache
from app.repositories.task_repository import (
    create_task as create_task_record,
    delete_task as delete_task_record,
    get_all_tasks,
    get_task_by_id,
    update_task as update_task_record,
)


async def create_task(
    db: AsyncSession,
    title: str,
    description: str | None,
    priority: str,
    completed: bool,
    owner_username: str,
):
    try:
        task = await create_task_record(
            db=db,
            title=title,
            description=description,
            priority=priority,
            completed=completed,
            owner_username=owner_username,
        )

        await create_task_history(
            db=db,
            task_id=task.id,
            action="created",
            description=f"Task '{task.title}' was created.",
        )

        await db.commit()
        await db.refresh(task)

        await invalidate_task_cache()

        return task

    except Exception:
        await db.rollback()
        raise


async def get_tasks(
    db: AsyncSession,
    owner_username: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    cache_key = (
        f"tasks:{owner_username or 'admin'}:"
        f"offset:{offset}:limit:{limit}"
    )

    cached_tasks = await get_cache(cache_key)

    if cached_tasks is not None:
        return cached_tasks

    tasks = await get_all_tasks(
        db=db,
        owner_username=owner_username,
        offset=offset,
        limit=limit,
    )

    task_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "completed": task.completed,
            "owner_username": task.owner_username,
        }
        for task in tasks
    ]

    await set_cache(
        key=cache_key,
        data=task_data,
        ttl=60,
    )

    return task_data


async def get_single_task(
    db: AsyncSession,
    task_id: int,
):
    return await get_task_by_id(
        db=db,
        task_id=task_id,
    )


async def update_task(
    db: AsyncSession,
    task_id: int,
    data: dict,
):
    task = await get_task_by_id(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return None

    try:
        await update_task_record(
            db=db,
            task=task,
            data=data,
        )

        await create_task_history(
            db=db,
            task_id=task.id,
            action="updated",
            description=f"Task '{task.title}' was updated.",
        )

        await db.commit()
        await db.refresh(task)

        await invalidate_task_cache()

        return task

    except Exception:
        await db.rollback()
        raise


async def remove_task(
    db: AsyncSession,
    task_id: int,
):
    task = await get_task_by_id(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return None

    try:
        task_title = task.title

        await create_task_history(
            db=db,
            task_id=task.id,
            action="deleted",
            description=f"Task '{task_title}' was deleted.",
        )

        await delete_task_record(
            db=db,
            task=task,
        )

        await db.commit()

        await invalidate_task_cache()

        return task

    except Exception:
        await db.rollback()
        raise