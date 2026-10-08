from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate


def task_to_dict(task: Task) -> dict:
    """
    Convert SQLAlchemy Task object into the Day 6 API format.
    """

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": task.completed,
        "owner_id": task.user_id,
    }


async def create_task(
    db: AsyncSession,
    task_data: TaskCreate,
    owner_id: int,
    ):
    task = await task_repository.create_task(
        db,
        user_id=owner_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status="completed" if task_data.completed else "pending",
    )

    return task_to_dict(task)

async def get_tasks(
    db: AsyncSession,
    *,
    page: int = 1,
    page_size: int = 10,
  ):
    offset = (page - 1) * page_size

    tasks = await task_repository.get_tasks(
        db,
        offset=offset,
        limit=page_size,
    )

    total = await task_repository.count_tasks(db)

    return {
        "items": [
            task_to_dict(task)
            for task in tasks
        ],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


async def get_task(
    db: AsyncSession,
    task_id: int,
):
    task = await task_repository.get_task_by_id(
        db,
        task_id,
    )

    if task is None:
        return None

    return task_to_dict(task)


async def get_user_tasks(
    db: AsyncSession,
    owner_id: int,
    *,
    page: int = 1,
    page_size: int = 10,
):
    offset = (page - 1) * page_size

    tasks = await task_repository.get_user_tasks(
        db,
        user_id=owner_id,
        offset=offset,
        limit=page_size,
    )

    total = await task_repository.count_user_tasks(
        db,
        user_id=owner_id,
    )

    return {
        "items": [
            task_to_dict(task)
            for task in tasks
        ],
        "page": page,
        "page_size": page_size,
        "total": total,
    }




async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskUpdate,
    changed_by: int,
   ):
    task = await task_repository.get_task_by_id(
        db,
        task_id,
    )

    if task is None:
        return None

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    old_status = task.status

    # Convert Day 6 "completed" into Day 7 "status"
    if "completed" in update_data:
        completed = update_data.pop("completed")

        update_data["status"] = (
            "completed"
            if completed
            else "pending"
        )

    try:
        await task_repository.update_task(
            db,
            task,
            title=update_data.get("title"),
            description=update_data.get("description"),
            priority=update_data.get("priority"),
            status=update_data.get("status"),
        )

        # Read the status AFTER the repository update.
        new_status = task.status

        # Create history only when the status actually changes.
        if old_status != new_status:
            from app.repositories import task_history_repository

            await task_history_repository.create_task_history(
                db,
                task_id=task.id,
                changed_by=changed_by,
                old_status=old_status,
                new_status=new_status,
            )

    except Exception:
        # Task update and history insertion must succeed
        # together. If either fails, rollback both.
        await db.rollback()
        raise

    return task_to_dict(task)

async def delete_task(
    db: AsyncSession,
    task_id: int,
):
    task = await task_repository.get_task_by_id(
        db,
        task_id,
    )

    if task is None:
        return None

    await task_repository.delete_task(
        db,
        task,
    )

    return task_to_dict(task)