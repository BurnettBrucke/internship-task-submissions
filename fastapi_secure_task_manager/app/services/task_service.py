from app.data.store import (
    add_task,
    delete_task,
    get_all_tasks,
    get_task,
)


def create_task(
    title: str,
    description: str | None,
    priority: str,
    completed: bool,
    owner_username: str,
):
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "completed": completed,
        "owner_username": owner_username,
    }

    return add_task(task)


def get_tasks():
    return get_all_tasks()


def get_single_task(task_id: int):
    return get_task(task_id)


def update_task(task_id: int, data: dict):
    task = get_task(task_id)

    if task is None:
        return None

    task.update(data)

    return task


def remove_task(task_id: int):
    return delete_task(task_id)