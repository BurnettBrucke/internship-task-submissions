import pytest

from app.database import AsyncSessionLocal
from app.services import task_service


@pytest.mark.asyncio
async def test_task_update_rolls_back_when_history_fails():
    async with AsyncSessionLocal() as db:

        # Get an existing task
        task = await task_service.get_single_task(db, 5)

        if task is None:
            pytest.skip("Task 5 not found")

        # Store values before update
        task_id = task.id
        user_id = task.user_id
        original_status = task.status

        # Function that will intentionally fail
        async def failing_history(*args, **kwargs):
            raise Exception("Simulated history failure")

        # Save original history function
        original_history_function = task_service.create_task_history

        # Replace history creation with failing function
        task_service.create_task_history = failing_history

        try:
            # Choose a different status
            new_status = (
                "in_progress"
                if original_status != "in_progress"
                else "pending"
            )

            # Update should fail because history creation fails
            with pytest.raises(
                Exception,
                match="Simulated history failure",
            ):
                await task_service.update_task(
                    db=db,
                    task_id=task_id,
                    changed_by=user_id,
                    data={
                        "status": new_status,
                    },
                )

        finally:
            # Restore original function
            task_service.create_task_history = original_history_function

        # Verify database still has original status
        task_after = await task_service.get_single_task(
            db,
            task_id,
        )

        assert task_after is not None
        assert task_after.status == original_status