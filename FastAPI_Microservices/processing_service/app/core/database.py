from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from processing_service.app.core.config import settings
from processing_service.app.models.job import Base


# Create database engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
)


# Create a session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_tables():
    """Create all database tables."""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_db_session():
    """Provide a database session for a request."""

    async with AsyncSessionLocal() as session:
        yield session