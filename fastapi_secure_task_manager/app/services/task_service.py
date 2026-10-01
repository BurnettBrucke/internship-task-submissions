from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.task_history import TaskHistory
from app.repositories.task_history_repository import TaskHistoryRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskListResponse
from app.services.task_cache import (
    get_cached_tasks,
    invalidate_tasks_cache,
    set_cached_tasks,
)

import logging
logger = logging.getLogger(__name__)

async def create_task(
    session: AsyncSession,
    title: str,
    description: str | None,
    priority: str,
    status: str,
    owner_id: int,
) -> Task:
    repository = TaskRepository(session)

    task = Task(
        user_id=owner_id,
        title=title,
        description=description,
        priority=priority,
        status=status,
    )

    try:
        await repository.create(task)

        await session.commit()
        await session.refresh(task)

    except Exception:
        await session.rollback()
        raise

    # The user's task list has changed.
    # Remove the old cached version only after a successful commit.
    await invalidate_tasks_cache(owner_id)

    return task


async def get_all_tasks(
    session: AsyncSession,
    current_user,
    search: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    repository = TaskRepository(session)

    # We use the required cache key:
    # tasks:user:{user_id}
    #
    # Only the default first page for a normal user is cached.
    # Admin results and filtered/paginated variants bypass this cache
    # because they would otherwise need different cache keys.
    cacheable = (
        current_user.role != "admin"
        and search is None
        and priority is None
        and status is None
        and page == 1
        and page_size == 10
    )

    if cacheable:
        cached_data = await get_cached_tasks(current_user.id)
    
        if cached_data is not None:
            logger.info(
                "Task cache HIT: tasks:user:%s",
                current_user.id,
            )
            return cached_data
    
        logger.info(
            "Task cache MISS: tasks:user:%s",
            current_user.id,
        )

    # Normal users see only their own tasks.
    # Admin users can see all tasks.
    user_id = None

    if current_user.role != "admin":
        user_id = current_user.id

    total = await repository.count_tasks(
        user_id=user_id,
        status=status,
        priority=priority,
        search=search,
    )

    tasks = await repository.list_tasks(
        page=page,
        page_size=page_size,
        user_id=user_id,
        status=status,
        priority=priority,
        search=search,
    )

    response_data = {
        "items": tasks,
        "page": page,
        "page_size": page_size,
        "total": total,
    }

    if cacheable:
        # Convert SQLAlchemy ORM objects into JSON-safe data
        # before storing them in Redis.
        cache_payload = (
            TaskListResponse
            .model_validate(response_data)
            .model_dump(mode="json")
        )

        await set_cached_tasks(
            current_user.id,
            cache_payload,
        )

    return response_data


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
    current_user,
) -> tuple[Task | None, str | None]:
    repository = TaskRepository(session)

    task = await repository.get_by_id(task_id)

    if task is None:
        return None, "not_found"

    # Normal users can only access their own tasks.
    # Admins can access any task.
    if current_user.role != "admin" and task.user_id != current_user.id:
        return None, "forbidden"

    return task, None


async def update_task(
    session: AsyncSession,
    task_id: int,
    current_user,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    status: str | None = None,
) -> tuple[Task | None, str | None]:
    task_repository = TaskRepository(session)
    history_repository = TaskHistoryRepository(session)

    task = await task_repository.get_by_id(task_id)

    if task is None:
        return None, "not_found"

    # Normal users cannot modify another user's task.
    # Admins can modify any task.
    if current_user.role != "admin" and task.user_id != current_user.id:
        return None, "forbidden"

    old_status = task.status

    status_changed = (
        status is not None
        and status != old_status
    )

    try:
        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        if priority is not None:
            task.priority = priority

        if status_changed:
            task.status = status

            history = TaskHistory(
                task_id=task.id,
                changed_by=current_user.id,
                old_status=old_status,
                new_status=status,
            )

            await history_repository.create(history)

        await task_repository.update(task)

        # Task update + history insertion are committed together.
        await session.commit()

        await session.refresh(task)

    except Exception:
        # If either the task update or history insert fails,
        # roll back the entire transaction.
        await session.rollback()
        raise

    # Invalidate the cache belonging to the task owner,
    # not the admin who may have performed the update.
    await invalidate_tasks_cache(task.user_id)

    return task, None


async def delete_task(
    session: AsyncSession,
    task_id: int,
    current_user,
) -> tuple[Task | None, str | None]:
    repository = TaskRepository(session)

    task = await repository.get_by_id(task_id)

    if task is None:
        return None, "not_found"

    # Normal users cannot delete another user's task.
    # Admins can delete any task.
    if current_user.role != "admin" and task.user_id != current_user.id:
        return None, "forbidden"

    owner_id = task.user_id

    try:
        await repository.delete(task)

        await session.commit()

    except Exception:
        await session.rollback()
        raise

    # Invalidate the cache belonging to the task owner.
    await invalidate_tasks_cache(owner_id)

    return task, None