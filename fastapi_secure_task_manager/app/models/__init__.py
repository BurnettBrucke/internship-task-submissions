# ============================================================
# REGISTER ALL DATABASE MODELS
# ============================================================

from app.models.base import Base
from app.models.user import User
from app.models.task import Task
from app.models.task_history import TaskHistory


__all__ = [
    "Base",
    "User",
    "Task",
    "TaskHistory",
]