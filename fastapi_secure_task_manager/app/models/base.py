# ============================================================
# SQLALCHEMY BASE MODEL
# ============================================================

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    User, Task, and TaskHistory models will inherit
    from this class.
    """

    pass