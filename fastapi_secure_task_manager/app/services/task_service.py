# ============================================================
# TASK SERVICE
# ============================================================
#
# Business logic layer.
#
# Flow:
# API Router
#      ↓
# Task Service
#      ↓
# Task Repository
#      ↓
# PostgreSQL
#
# Redis is used as a cache for task listing.
#
# ============================================================

import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.redis import redis_client

from app.repositories.task_repository import (
    create_task as repo_create_task,
    get_task_by_id,
    get_tasks,
    count_tasks,
    update_task as repo_update_task,
    delete_task as repo_delete_task,
    create_task_history,
    get_user_by_username,
)

from app.schemas.task import TaskCreate, TaskUpdate

def invalidate_user_task_cache(user_id: int):
    pattern = f"tasks:user:{user_id}:*"

    keys = redis_client.keys(pattern)

    if keys:
        redis_client.delete(*keys)


# ============================================================
# HELPER: DATABASE TASK → API RESPONSE
# ============================================================

def task_to_response(task, owner_username: str) -> dict:
    """
    Convert SQLAlchemy Task object into the response format
    used by the existing Day 6 API.
    """

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": task.status == "completed",
        "owner_username": owner_username,
    }


# ============================================================
# CREATE TASK
# ============================================================

async def create_task(
    db: AsyncSession,
    task: TaskCreate,
    owner_username: str,
) -> dict:
    """
    Create a task in PostgreSQL.
    """

    user = await get_user_by_username(
        db,
        username=owner_username,
    )

    if user is None:
        raise ValueError("User not found")

    task_status = (
        "completed"
        if task.completed
        else "pending"
    )

    db_task = await repo_create_task(
        db,
        user_id=user.id,
        title=task.title,
        description=task.description,
        priority=task.priority.value,
        status=task_status,
    )

    await db.commit()

    invalidate_user_task_cache(user.id)

    return task_to_response(db_task, owner_username=user.username)


# ============================================================
# GET ALL TASKS
# ============================================================

async def get_all_tasks(
    db: AsyncSession,
    owner_username: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    """
    Get paginated tasks.

    If owner_username is provided:
        Return only that user's tasks.

    If owner_username is None:
        Return all tasks (admin).
    """

    user_id = None
    cache_key = None

    # --------------------------------------------------------
    # NORMAL USER
    # --------------------------------------------------------

    if owner_username is not None:

        user = await get_user_by_username(
            db,
            username=owner_username,
        )

        if user is None:
            raise ValueError("User not found")

        user_id = user.id

        # Redis cache key
        cache_key = (
            f"tasks:user:{user_id}:"
            f"page:{page}:size:{page_size}"
        )

        # Check Redis cache
        cached_data = redis_client.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

    # --------------------------------------------------------
    # DATABASE QUERY
    # --------------------------------------------------------

    offset = (page - 1) * page_size

    db_tasks = await get_tasks(
        db,
        user_id=user_id,
        offset=offset,
        limit=page_size,
    )

    # Get total count
    total = await count_tasks(
        db,
        user_id=user_id,
    )

    # --------------------------------------------------------
    # CONVERT DATABASE TASKS → API RESPONSE
    # --------------------------------------------------------

    items = []

    for db_task in db_tasks:

        owner = db_task.owner

        items.append(
            task_to_response(
                db_task,
                owner_username=owner.username,
            )
        )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    result = {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }

    # --------------------------------------------------------
    # SAVE RESPONSE IN REDIS
    # --------------------------------------------------------

    if cache_key:

        redis_client.setex(
            cache_key,
            settings.CACHE_TTL_SECONDS,
            json.dumps(result),
        )

    return result


# ============================================================
# GET SINGLE TASK
# ============================================================

async def get_task(
    db: AsyncSession,
    task_id: int,
) -> dict | None:
    """
    Get one task by ID.
    """

    db_task = await get_task_by_id(
        db,
        task_id=task_id,
    )

    if db_task is None:
        return None

    owner = db_task.owner

    return task_to_response(
        db_task,
        owner_username=owner.username,
    )


# ============================================================
# UPDATE TASK
# ============================================================

async def update_task(
    db: AsyncSession,
    task_id: int,
    task: TaskUpdate,
    changed_by: int,
) -> dict | None:
    """
    Update an existing task.

    If the status/completed value changes:
        1. Update task
        2. Create task_history
        3. Commit both together

    If history creation fails:
        The transaction is rolled back.
    """

    db_task = await get_task_by_id(
        db,
        task_id=task_id,
    )

    if db_task is None:
        return None

    old_status = db_task.status

    update_data = task.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Convert completed → status
    # --------------------------------------------------------

    new_status = None

    if "completed" in update_data:

        completed = update_data.pop("completed")

        new_status = (
            "completed"
            if completed
            else "pending"
        )

    # --------------------------------------------------------
    # Extract normal fields
    # --------------------------------------------------------

    title = update_data.get("title")
    description = update_data.get("description")
    priority = update_data.get("priority")

    if priority is not None:
        priority = priority.value

    # --------------------------------------------------------
    # Check whether status actually changed
    # --------------------------------------------------------

    status_changed = (
        new_status is not None
        and new_status != old_status
    )

    try:

        # ----------------------------------------------------
        # Update task
        # ----------------------------------------------------

        await repo_update_task(
            db,
            task=db_task,
            title=title,
            description=description,
            priority=priority,
            status=new_status,
        )

        # ----------------------------------------------------
        # Create history if status changed
        # ----------------------------------------------------

        if status_changed:

            await create_task_history(
                db,
                task_id=db_task.id,
                changed_by=changed_by,
                old_status=old_status,
                new_status=new_status,
            )

        # ----------------------------------------------------
        # Commit BOTH operations together
        # ----------------------------------------------------

        await db.commit()

        invalidate_user_task_cache(db_task.user_id)

    except Exception:

        # ----------------------------------------------------
        # Rollback if anything fails
        # ----------------------------------------------------

        await db.rollback()
        raise

    # Refresh after successful transaction
    await db.refresh(db_task)

    owner = db_task.owner

    return task_to_response(
        db_task,
        owner_username=owner.username,
    )


# ============================================================
# DELETE TASK
# ============================================================

async def delete_task(
    db: AsyncSession,
    task_id: int,
) -> bool:
    """
    Delete a task from PostgreSQL.
    """

    db_task = await get_task_by_id(
        db,
        task_id=task_id,
    )

    if db_task is None:
        return False

    try:

        await repo_delete_task(
            db,
            task=db_task,
        )

        await db.commit()

        invalidate_user_task_cache(db_task.user_id)

    except Exception:

        await db.rollback()
        raise

    return True