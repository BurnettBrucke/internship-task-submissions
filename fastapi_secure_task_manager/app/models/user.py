# ============================================================
# USER DATABASE MODEL
# ============================================================

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    """
    SQLAlchemy model for the users table.
    """

    __tablename__ = "users"

    # --------------------------------------------------------
    # Primary Key
    # --------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # --------------------------------------------------------
    # User Information
    # --------------------------------------------------------

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # --------------------------------------------------------
    # Role
    # --------------------------------------------------------

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="user",
    )

    # --------------------------------------------------------
    # Account Status
    # --------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # --------------------------------------------------------
    # Created At
    # --------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
    	DateTime,
    	nullable=True
    )

    # --------------------------------------------------------
    # Relationship
    # --------------------------------------------------------

    tasks = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan",
    )