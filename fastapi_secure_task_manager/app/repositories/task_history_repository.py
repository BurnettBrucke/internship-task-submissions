from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_history import TaskHistory


class TaskHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, history: TaskHistory) -> TaskHistory:
        self.session.add(history)

        await self.session.flush()

        return history