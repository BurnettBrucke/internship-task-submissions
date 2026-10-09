"""add task history changed_at default

Revision ID: b26424c5ac62
Revises: 6470c9785495
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b26424c5ac62"
down_revision: Union[str, Sequence[str], None] = "6470c9785495"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "task_history",
        "changed_at",
        server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column(
        "task_history",
        "changed_at",
        server_default=None,
    )