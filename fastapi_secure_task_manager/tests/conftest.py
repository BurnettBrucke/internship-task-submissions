import asyncio
import os

import pytest
import redis
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

load_dotenv()

from app.core.config import settings
from app.db.database import get_db
from app.main import app
from app.models.task import Task
from app.models.task_history import TaskHistory
from app.models.user import User


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL is required when running tests."
    )


test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    pool_pre_ping=True,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


async def clear_database():
    async with TestSessionLocal() as db:
        await db.execute(delete(TaskHistory))
        await db.execute(delete(Task))
        await db.execute(delete(User))
        await db.commit()


def clear_redis_task_cache():
    redis_client = redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )

    keys = list(
        redis_client.scan_iter(
            match="tasks:user:*"
        )
    )

    if keys:
        redis_client.delete(*keys)

    redis_client.close()


@pytest.fixture(scope="session", autouse=True)
def configure_test_database():
    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.pop(
        get_db,
        None,
    )

    asyncio.run(
        test_engine.dispose()
    )


@pytest.fixture(autouse=True)
def clean_test_data():
    asyncio.run(
        clear_database()
    )

    clear_redis_task_cache()

    yield

    asyncio.run(
        clear_database()
    )

    clear_redis_task_cache()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client