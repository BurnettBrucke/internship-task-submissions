import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.db.database import get_db
from app.main import app
from app.models.task import Task
from app.models.task_history import TaskHistory
from app.models.user import User
from app.services.auth_service import login_attempts

from app.cache.redis import redis_client

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL environment variable is required."
    )


test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


async def clean_database():
    async with TestSessionLocal() as session:
        # Foreign-key dependent tables must be deleted first.
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


@pytest_asyncio.fixture(autouse=True)
async def database_cleanup():
    await clean_database()
    await clean_redis()
    login_attempts.clear()

    yield

    await clean_database()
    await clean_redis()
    login_attempts.clear()
    
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session

async def clean_redis():
    keys = [
        key
        async for key in redis_client.scan_iter(
            match="tasks:user:*"
        )
    ]

    if keys:
        await redis_client.delete(*keys)