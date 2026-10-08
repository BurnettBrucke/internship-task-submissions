from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

from app.core.config import settings
from app.db.database import Base

# Import all models so SQLAlchemy registers them in Base.metadata.
from app.models import User, Task, TaskHistory  # noqa: F401


# Alembic Config object
config = context.config


# Configure Python logging from alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata used by Alembic for autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.

    Alembic generates SQL statements instead of executing them.
    """

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Configure Alembic using an already-created database connection.
    """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Create an async SQLAlchemy engine and run Alembic migrations.
    """

    connectable: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations
        )

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations against the live PostgreSQL database.
    """

    import asyncio

    asyncio.run(
        run_async_migrations()
    )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()