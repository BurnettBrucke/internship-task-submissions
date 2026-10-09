"""add idempotency key to jobs

Revision ID: 7565162fa9cd
Revises: 2d2c156223af
Create Date: 2026-10-06 18:00:17.525561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7565162fa9cd'
down_revision: Union[str, Sequence[str], None] = '2d2c156223af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "jobs",
        sa.Column(
            "idempotency_key",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.execute(
        "UPDATE jobs SET idempotency_key = job_id "
        "WHERE idempotency_key IS NULL"
    )

    op.alter_column(
        "jobs",
        "idempotency_key",
        nullable=False,
    )

    op.create_unique_constraint(
        "uq_jobs_idempotency_key",
        "jobs",
        ["idempotency_key"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_jobs_idempotency_key",
        "jobs",
        type_="unique",
    )

    op.drop_column(
        "jobs",
        "idempotency_key",
    )
