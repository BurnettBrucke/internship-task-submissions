# ============================================================
# DATABASE CONFIGURATION
# ============================================================

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


# ============================================================
# ASYNC DATABASE ENGINE
# ============================================================

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
)


# ============================================================
# ASYNC SESSION FACTORY
# ============================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ============================================================
# DATABASE SESSION DEPENDENCY
# ============================================================

async def get_db():
    """
    Provide an AsyncSession for database operations.
    The session is automatically closed after the request.
    """

    async with AsyncSessionLocal() as session:
        yield session