# ============================================================
# TASK HISTORY DATABASE MODEL
# ============================================================

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TaskHistory(Base):
    """
    SQLAlchemy model for the task_history table.

    Stores every task status change.
    """

    __tablename__ = "task_history"

    # --------------------------------------------------------
    # Primary Key
    # --------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # --------------------------------------------------------
    # Task Foreign Key
    # --------------------------------------------------------

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False,
        index=True,
    )

    # --------------------------------------------------------
    # User who changed the status
    # --------------------------------------------------------

    changed_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # Status Change Information
    # --------------------------------------------------------

    old_status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    new_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # --------------------------------------------------------
    # Timestamp
    # --------------------------------------------------------

    changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    # --------------------------------------------------------
    # Relationship with Task
    # --------------------------------------------------------

    task = relationship(
        "Task",
        back_populates="history",
    )