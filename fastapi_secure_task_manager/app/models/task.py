from datetime import date, datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym

from app.db.database import Base


class Task(Base):
    """
    SQLAlchemy model for the tasks table.

    Day 7 uses:
        user_id
        status
        created_at
        updated_at

    Day 6 exposed:
        owner_id
        completed

    We keep compatibility aliases/properties here so the service
    layer can continue supporting the Day 6 API contract.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    due_date: Mapped[date | None] = mapped_column(
        nullable=True
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Day 6 compatibility:
    # owner_id will behave as an alias for user_id.
    owner_id = synonym("user_id")

    # Relationship to the User model.
    user = relationship(
        "User",
        lazy="selectin"
    )

    @property
    def completed(self) -> bool:
        """
        Day 6 compatibility property.

        Day 6 used a boolean:
            completed = True / False

        Day 7 uses a status string.
        """
        return self.status == "completed"

    @completed.setter
    def completed(self, value: bool) -> None:
        """
        Convert the Day 6 boolean representation into
        the Day 7 status representation.
        """
        self.status = "completed" if value else "pending"

    __table_args__ = (
        Index(
            "ix_tasks_user_id",
            "user_id"
        ),
        Index(
            "ix_tasks_status",
            "status"
        ),
    )