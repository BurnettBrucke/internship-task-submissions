from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from processing_service.app.models.base import Base



class Job(Base):
    __tablename__ = "jobs"

    job_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    job_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="CREATED",
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )