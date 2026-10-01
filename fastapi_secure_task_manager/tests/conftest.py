import asyncio

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db
from app.core.config import settings
from app.core.redis import redis_client
from app.models.task_history import TaskHistory
from app.models.task import Task
from app.models.user import User
from app.data.store import login_attempts


# ============================================================
# TEST DATABASE ENGINE
# ============================================================

test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ============================================================
# TEST DATABASE CLEANUP
# ============================================================

async def clean_database():
    async with TestSessionLocal() as session:

        # Delete child records first because of foreign keys
        await session.execute(
            delete(TaskHistory)
        )

        await session.execute(
            delete(Task)
        )

        await session.execute(
            delete(User)
        )

        await session.commit()


# ============================================================
# FASTAPI DATABASE OVERRIDE
# ============================================================

async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# ============================================================
# TEST CLIENT
# ============================================================

@pytest.fixture
def client():
    return TestClient(app)


# ============================================================
# CLEAN DATABASE BEFORE AND AFTER EVERY TEST
# ============================================================

@pytest.fixture(autouse=True)
def clean_test_environment():

    # Before test
    asyncio.run(clean_database())

    # Clear Day 6 login-attempt tracking
    login_attempts.clear()

    # Clear Redis cache
    redis_client.flushdb()

    yield

    # After test
    asyncio.run(clean_database())

    login_attempts.clear()

    redis_client.flushdb()