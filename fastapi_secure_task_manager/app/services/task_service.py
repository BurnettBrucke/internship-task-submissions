from app.data.store import tasks


def create_task(
    title: str,
    description: str | None,
    priority: str,
    completed: bool,
    owner_id: int,
):
    task_id = max(tasks.keys(), default=0) + 1

    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "completed": completed,
        "owner_id": owner_id,
    }

    tasks[task_id] = task

    return task


def can_access_task(task: dict, current_user: dict) -> bool:
    if current_user["role"] == "admin":
        return True

    return task["owner_id"] == current_user["id"]


def get_all_tasks(
    current_user: dict,
    search: str | None = None,
    priority: str | None = None,
    completed: bool | None = None,
    sort_by: str | None = None,
    page: int = 1,
    limit: int = 10,
):
    # Get tasks based on user role
    if current_user["role"] == "admin":
        user_tasks = list(tasks.values())
    else:
        user_tasks = [
            task
            for task in tasks.values()
            if task["owner_id"] == current_user["id"]
        ]

    # Search
    if search:
        search = search.lower()

        user_tasks = [
            task
            for task in user_tasks
            if search in task["title"].lower()
            or (
                task["description"]
                and search in task["description"].lower()
            )
        ]

    # Priority filter
    if priority:
        user_tasks = [
            task
            for task in user_tasks
            if task["priority"] == priority
        ]

    # Completed filter
    if completed is not None:
        user_tasks = [
            task
            for task in user_tasks
            if task["completed"] == completed
        ]

    # Sorting
    if sort_by:
        user_tasks.sort(
            key=lambda task: task[sort_by]
        )

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    return user_tasks[start:end]


def get_task_by_id(
    task_id: int,
    current_user: dict,
):
    task = tasks.get(task_id)

    if task is None:
        return None, "not_found"

    if not can_access_task(task, current_user):
        return None, "forbidden"

    return task, None


def update_task(
    task_id: int,
    current_user: dict,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    completed: bool | None = None,
):
    task = tasks.get(task_id)

    if task is None:
        return None, "not_found"

    if not can_access_task(task, current_user):
        return None, "forbidden"

    if title is not None:
        task["title"] = title

    if description is not None:
        task["description"] = description

    if priority is not None:
        task["priority"] = priority

    if completed is not None:
        task["completed"] = completed

    return task, None


def delete_task(
    task_id: int,
    current_user: dict,
):
    task = tasks.get(task_id)

    if task is None:
        return None, "not_found"

    if not can_access_task(task, current_user):
        return None, "forbidden"

    deleted_task = tasks.pop(task_id)

    return deleted_task, None