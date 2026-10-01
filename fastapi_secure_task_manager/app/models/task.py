# ============================================================
# TASK DATABASE MODEL
# ============================================================

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Task(Base):
    """
    SQLAlchemy model for the tasks table.
    """

    __tablename__ = "tasks"

    # --------------------------------------------------------
    # Primary Key
    # --------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # --------------------------------------------------------
    # Owner / Foreign Key
    # --------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # --------------------------------------------------------
    # Task Information
    # --------------------------------------------------------

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
    )

    # --------------------------------------------------------
    # Task Status
    # --------------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
    )

    # --------------------------------------------------------
    # Timestamps
    # --------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # --------------------------------------------------------
    # Relationships
    # --------------------------------------------------------

    owner = relationship(
        "User",
        back_populates="tasks",
    )

    history = relationship(
        "TaskHistory",
        back_populates="task",
        cascade="all, delete-orphan",
    )