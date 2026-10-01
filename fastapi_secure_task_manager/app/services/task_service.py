from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_history_repository import create_task_history
from app.repositories.task_repository import (
    count_tasks,
    create_task as create_task_record,
    delete_task as delete_task_record,
    get_task_by_id,
    get_tasks as get_task_records,
    update_task as update_task_record,
)
from app.services.cache_service import (
    get_cache,
    invalidate_task_cache,
    set_cache,
)


async def create_task(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str | None,
    priority: str,
    status: str,
):
    try:
        task = await create_task_record(
            db=db,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
        )

        await create_task_history(
            db=db,
            task_id=task.id,
            changed_by=user_id,
            old_status=None,
            new_status=status,
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
    user_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
):
    cache_user = user_id if user_id is not None else "admin"
    page = (offset // limit) + 1

    cache_key = f"tasks:user:{cache_user}:page:{page}:page_size:{limit}"

    cached_data = await get_cache(cache_key)

    if cached_data is not None:
        return cached_data

    tasks = await get_task_records(
        db=db,
        user_id=user_id,
        offset=offset,
        limit=limit,
    )

    total = await count_tasks(
        db=db,
        user_id=user_id,
    )

    task_data = [
        {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
        }
        for task in tasks
    ]

    response = {
        "items": task_data,
        "page": page,
        "page_size": limit,
        "total": total,
    }

    await set_cache(
        key=cache_key,
        data=response,
    )

    return response


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
    changed_by: int,
    data: dict,
):
    task = await get_task_by_id(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return None

    old_status = task.status
    new_status = data.get("status", old_status)

    try:
        await update_task_record(
            db=db,
            task=task,
            data=data,
        )

        if new_status != old_status:
            await create_task_history(
                db=db,
                task_id=task.id,
                changed_by=changed_by,
                old_status=old_status,
                new_status=new_status,
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