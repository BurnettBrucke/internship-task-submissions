from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(
        String(100),
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

    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    owner_username: Mapped[str] = mapped_column(
        ForeignKey("users.username"),
        nullable=False,
        index=True,
    )

    owner: Mapped["User"] = relationship(
        back_populates="tasks",
    )

    history: Mapped[list["TaskHistory"]] = relationship(
     back_populates="task",
    )