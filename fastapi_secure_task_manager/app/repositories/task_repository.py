from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.session.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_for_user(
        self,
        task_id: int,
        user_id: int,
    ) -> Task | None:
        result = await self.session.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.flush()
        return task

    async def update(self, task: Task) -> Task:
        await self.session.flush()
        return task

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.flush()

    async def count_tasks(
        self,
        user_id: int | None = None,
        status: str | None = None,
        priority: str | None = None,
        search: str | None = None,
    ) -> int:
        query = select(func.count(Task.id))

        if user_id is not None:
            query = query.where(Task.user_id == user_id)

        if status is not None:
            query = query.where(Task.status == status)

        if priority is not None:
            query = query.where(Task.priority == priority)

        if search:
            search_pattern = f"%{search}%"

            query = query.where(
                Task.title.ilike(search_pattern)
                | Task.description.ilike(search_pattern)
            )

        result = await self.session.execute(query)

        return result.scalar_one()

    async def list_tasks(
        self,
        page: int,
        page_size: int,
        user_id: int | None = None,
        status: str | None = None,
        priority: str | None = None,
        search: str | None = None,
    ) -> list[Task]:
        offset = (page - 1) * page_size

        query = select(Task)

        if user_id is not None:
            query = query.where(Task.user_id == user_id)

        if status is not None:
            query = query.where(Task.status == status)

        if priority is not None:
            query = query.where(Task.priority == priority)

        if search:
            search_pattern = f"%{search}%"

            query = query.where(
                Task.title.ilike(search_pattern)
                | Task.description.ilike(search_pattern)
            )

        query = (
            query
            .order_by(Task.created_at.desc(), Task.id.desc())
            .offset(offset)
            .limit(page_size)
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())