# ============================================================
# 1. IMPORTS
# ============================================================
from enum import Enum

from pydantic import BaseModel, Field


# ============================================================
# 2. TASK PRIORITY
# ============================================================
class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ============================================================
# 3. CREATE TASK
# ============================================================
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    completed: bool = False


# ============================================================
# 4. UPDATE TASK
# ============================================================
class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: TaskPriority | None = None
    completed: bool | None = None


# ============================================================
# 5. TASK RESPONSE
# ============================================================
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: TaskPriority
    completed: bool
    owner_username: str