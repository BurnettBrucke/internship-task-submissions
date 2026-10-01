# ============================================================
# ALEMBIC CONFIGURATION
# ============================================================

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.models.base import Base

# Import all models so SQLAlchemy registers them
from app.models.user import User
from app.models.task import Task
from app.models.task_history import TaskHistory


# ============================================================
# ALEMBIC CONFIG OBJECT
# ============================================================

config = context.config


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ============================================================
# DATABASE URL
# ============================================================

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("%", "%%")
)


# ============================================================
# SQLALCHEMY METADATA
# ============================================================

target_metadata = Base.metadata


# ============================================================
# OFFLINE MIGRATIONS
# ============================================================

def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.
    """

    url = settings.DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# ONLINE MIGRATIONS
# ============================================================

def do_run_migrations(connection) -> None:
    """
    Configure Alembic with an active database connection.
    """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Create an async SQLAlchemy engine and run migrations.
    """

    connectable = async_engine_from_config(
        config.get_section(
            config.config_ini_section,
            {},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations
        )

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run Alembic migrations using async SQLAlchemy.
    """

    import asyncio

    asyncio.run(
        run_async_migrations()
    )


# ============================================================
# START MIGRATION
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()