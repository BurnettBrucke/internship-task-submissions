from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_history import TaskHistory


async def create_task_history(
    db: AsyncSession,
    task_id: int,
    changed_by: int,
    old_status: str | None,
    new_status: str,
):
    history = TaskHistory(
        task_id=task_id,
        changed_by=changed_by,
        old_status=old_status,
        new_status=new_status,
    )

    db.add(history)
    await db.flush()

    return history