from app.data.store import tasks_db
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(task: TaskCreate, owner_username: str) -> dict:
    from app.data.store import next_task_id

    task_id = next_task_id

    tasks_db[task_id] = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority.value,
        "completed": task.completed,
        "owner_username": owner_username,
    }

    # Increase ID for the next task
    import app.data.store as store
    store.next_task_id += 1

    return tasks_db[task_id]

def get_all_tasks(owner_username: str | None = None) -> list:
    if owner_username:
        return [
            task
            for task in tasks_db.values()
            if task["owner_username"] == owner_username
        ]

    return list(tasks_db.values())


def get_task(task_id: int) -> dict | None:
    return tasks_db.get(task_id)


def update_task(task_id: int, task: TaskUpdate) -> dict | None:
    existing_task = tasks_db.get(task_id)

    if existing_task is None:
        return None

    update_data = task.model_dump(exclude_unset=True)

    if "priority" in update_data:
        update_data["priority"] = update_data["priority"].value

    existing_task.update(update_data)

    return existing_task


def delete_task(task_id: int) -> bool:
    if task_id not in tasks_db:
        return False

    del tasks_db[task_id]

    return True