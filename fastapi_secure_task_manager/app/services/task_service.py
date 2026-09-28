from app.data.store import tasks
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(
    task_data: TaskCreate,
    owner_id: int
):
    new_id = (
        max(task["id"] for task in tasks) + 1
        if tasks
        else 1
    )

    new_task = {
        "id": new_id,
        "title": task_data.title,
        "description": task_data.description,
        "priority": task_data.priority,
        "completed": task_data.completed,
        "owner_id": owner_id,
    }

    tasks.append(new_task)

    return new_task


def get_tasks():
    return tasks


def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None


def get_user_tasks(owner_id: int):
    return [
        task
        for task in tasks
        if task["owner_id"] == owner_id
    ]


def update_task(
    task_id: int,
    task_data: TaskUpdate
):
    task = get_task(task_id)

    if task is None:
        return None

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    task.update(update_data)

    return task


def delete_task(task_id: int):
    task = get_task(task_id)

    if task is None:
        return None

    tasks.remove(task)

    return task