from datetime import datetime

users = {}
tasks = {}

login_attempts = {}
login_blocked_until = {}

next_task_id = 1


def get_user(username: str):
    return users.get(username)


def add_user(user: dict):
    users[user["username"]] = user


def get_login_attempts(username: str):
    return login_attempts.get(username, 0)


def set_login_attempts(username: str, attempts: int):
    login_attempts[username] = attempts


def get_blocked_until(username: str):
    return login_blocked_until.get(username)


def set_blocked_until(username: str, blocked_until: datetime):
    login_blocked_until[username] = blocked_until


def clear_login_security(username: str):
    login_attempts.pop(username, None)
    login_blocked_until.pop(username, None)


def get_task(task_id: int):
    return tasks.get(task_id)


def get_all_tasks():
    return list(tasks.values())


def add_task(task: dict):
    global next_task_id

    task["id"] = next_task_id
    next_task_id += 1

    tasks[task["id"]] = task
    return task


def delete_task(task_id: int):
    return tasks.pop(task_id, None)