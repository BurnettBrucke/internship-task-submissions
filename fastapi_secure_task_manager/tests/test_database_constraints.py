import pytest
from sqlalchemy.exc import IntegrityError

from app.database import AsyncSessionLocal
from app.models.task import Task


@pytest.mark.asyncio
async def test_invalid_foreign_key():
    async with AsyncSessionLocal() as db:
        task = Task(
            user_id=999999999,
            title="Invalid FK Test",
            description="Testing invalid user foreign key",
            priority="medium",
            status="pending",
        )

        db.add(task)

        with pytest.raises(IntegrityError):
            await db.commit()

        await db.rollback()