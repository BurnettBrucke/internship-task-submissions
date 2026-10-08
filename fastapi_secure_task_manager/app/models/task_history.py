from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TaskHistory(Base):
    """
    Stores every task status change.

    A history record is created whenever a task's status changes.
    """

    __tablename__ = "task_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    changed_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    old_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    new_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    task = relationship(
        "Task",
        lazy="selectin"
    )

    user = relationship(
        "User",
        lazy="selectin"
    )