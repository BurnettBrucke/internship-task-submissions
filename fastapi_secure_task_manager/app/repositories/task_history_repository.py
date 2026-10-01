from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_history import TaskHistory


async def create_task_history(
    db: AsyncSession,
    task_id: int,
    action: str,
    description: str | None = None,
):
    history = TaskHistory(
        task_id=task_id,
        action=action,
        description=description,
    )

    db.add(history)

    return history