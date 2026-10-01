from datetime import datetime

from sqlalchemy import Boolean , DateTime , String , UniqueConstraint , func
from sqlalchemy.orm import Mapped , mapped_column , relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    __table_args__ = (UniqueConstraint("email" , name = "uq_users_email"),)

    id : Mapped[int] = mapped_column(
        primary_key= True,
    )

    username : Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable= False,
        index = True
    )

    email : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="user",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True,
            )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    task_history_changes: Mapped[list["TaskHistory"]] = relationship(
        back_populates="changed_by_user",
        foreign_keys="TaskHistory.changed_by",
    )
