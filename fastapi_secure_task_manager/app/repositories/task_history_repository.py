from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_history import TaskHistory


async def create_task_history(
    db: AsyncSession,
    *,
    task_id: int,
    changed_by: int,
    old_status: str,
    new_status: str,
) -> TaskHistory:
    history = TaskHistory(
        task_id=task_id,
        changed_by=changed_by,
        old_status=old_status,
        new_status=new_status,
    )

    db.add(history)

    # Send INSERT to PostgreSQL without committing.
    # The service/router transaction will control the commit.
    await db.flush()
    await db.refresh(history)

    return history