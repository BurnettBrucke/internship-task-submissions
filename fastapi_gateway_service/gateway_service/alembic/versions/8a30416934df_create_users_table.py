"""create users table

Revision ID: 8a30416934df
Revises: 00f297d7b0d1
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "8a30416934df"
down_revision: str | Sequence[str] | None = "00f297d7b0d1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_users_username",
        "users",
        ["username"],
        unique=True,
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")