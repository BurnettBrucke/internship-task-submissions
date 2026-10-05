from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped , mapped_column

from app.db.base import Base

from app.schemas.job import JobType , JobPriority , JobStatus

class Job(Base):
    __tablename__ = "jobs"

    id : Mapped[int]=mapped_column(
        primary_key=True , autoincrement=True
    )
    name : Mapped[str]=mapped_column(
        String(255) , nullable=False
    )
    job_type : Mapped[JobType]=mapped_column(
        SqlEnum(JobType) , nullable=False
    )
    priority : Mapped[JobPriority]=mapped_column(
        SqlEnum(JobPriority) , nullable=False
    )
    status : Mapped[JobStatus]=mapped_column(
        SqlEnum(JobStatus) , nullable=False,
        default=JobStatus.CREATED

    )