from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TaskHistory(Base):
    __tablename__ = "task_history"

    __table_args__ = (
        Index(
            "ix_task_history_task_id",
            "task_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    changed_by: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    old_status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    new_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    task: Mapped["Task"] = relationship(
        back_populates="history",
    )

    changed_by_user: Mapped["User"] = relationship(
        back_populates="task_history_changes",
        foreign_keys=[changed_by],
    )