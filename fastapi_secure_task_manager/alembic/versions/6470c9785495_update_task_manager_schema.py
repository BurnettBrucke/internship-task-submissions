"""update task manager schema

Revision ID: 6470c9785495
Revises: 850f6e120ebc
Create Date: 2026-10-01 12:04:53.250916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6470c9785495"
down_revision: Union[str, Sequence[str], None] = "850f6e120ebc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # 1. USERS - add new columns
    # ---------------------------------------------------------
    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    # Existing users should remain active.
    op.execute(
        "UPDATE users SET is_active = TRUE WHERE is_active IS NULL"
    )

    op.alter_column(
        "users",
        "is_active",
        nullable=False,
    )

    op.alter_column(
        "users",
        "created_at",
        nullable=False,
    )

    # Email already has a unique constraint.
    # Keep it as-is; no duplicate unique index is required.


    # ---------------------------------------------------------
    # 2. TASKS - add new columns
    # ---------------------------------------------------------
    op.add_column(
        "tasks",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 3. TASKS - migrate existing owner_username -> user_id
    # ---------------------------------------------------------
    op.execute(
        """
        UPDATE tasks
        SET user_id = users.id
        FROM users
        WHERE tasks.owner_username = users.username
        """
    )

    # Existing completed boolean -> status
    op.execute(
        """
        UPDATE tasks
        SET status = CASE
            WHEN completed = TRUE THEN 'completed'
            ELSE 'pending'
        END
        """
    )

    # Existing rows already have timestamps through server defaults.
    # Make sure no NULL values remain.
    op.execute(
        """
        UPDATE tasks
        SET created_at = COALESCE(created_at, now()),
            updated_at = COALESCE(updated_at, now())
        """
    )

    # ---------------------------------------------------------
    # 4. TASKS - create new indexes
    # ---------------------------------------------------------
    op.create_index(
        "ix_tasks_user_id",
        "tasks",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_tasks_status",
        "tasks",
        ["status"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 5. TASKS - create new FK
    # ---------------------------------------------------------
    op.create_foreign_key(
        "fk_tasks_user_id_users",
        "tasks",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Now values are guaranteed for existing records.
    op.alter_column(
        "tasks",
        "user_id",
        nullable=False,
    )

    op.alter_column(
        "tasks",
        "status",
        nullable=False,
    )

    op.alter_column(
        "tasks",
        "created_at",
        nullable=False,
    )

    op.alter_column(
        "tasks",
        "updated_at",
        nullable=False,
    )


    # ---------------------------------------------------------
    # 6. TASK HISTORY - add new columns
    # ---------------------------------------------------------
    op.add_column(
        "task_history",
        sa.Column(
            "changed_by",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "task_history",
        sa.Column(
            "old_status",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.add_column(
        "task_history",
        sa.Column(
            "new_status",
            sa.String(length=20),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 7. TASK HISTORY - migrate existing history
    # ---------------------------------------------------------

    # Remove history records of tasks that were already deleted.
    op.execute(
        """
        DELETE FROM task_history
        WHERE task_id IS NULL
        """
    )
    
    # Existing history belongs to the task owner.
    op.execute(
        """
        UPDATE task_history
        SET changed_by = tasks.user_id
        FROM tasks
        WHERE task_history.task_id = tasks.id
        """
    )


    # Old "created" records have no previous status.
    # Existing completed value is used as current/new status.
    op.execute(
        """
        UPDATE task_history
        SET new_status = CASE
            WHEN tasks.completed = TRUE THEN 'completed'
            ELSE 'pending'
        END
        FROM tasks
        WHERE task_history.task_id = tasks.id
          AND task_history.new_status IS NULL
        """
    )

    # For old records where task still exists.
    op.execute(
        """
        UPDATE task_history
        SET old_status = CASE
            WHEN new_status = 'completed' THEN 'pending'
            ELSE NULL
        END
        WHERE old_status IS NULL
        """
    )

    # ---------------------------------------------------------
    # 8. TASK HISTORY - indexes
    # ---------------------------------------------------------
    op.create_index(
        "ix_task_history_changed_by",
        "task_history",
        ["changed_by"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 9. TASK HISTORY - new foreign keys
    # ---------------------------------------------------------
    # Replace old SET NULL FK with CASCADE FK.
    op.drop_constraint(
        "task_history_task_id_fkey",
        "task_history",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_task_history_task_id_tasks",
        "task_history",
        "tasks",
        ["task_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "fk_task_history_changed_by_users",
        "task_history",
        "users",
        ["changed_by"],
        ["id"],
        ondelete="CASCADE",
    )

    op.alter_column(
        "task_history",
        "task_id",
        nullable=False,
    )

    op.alter_column(
        "task_history",
        "new_status",
        nullable=False,
    )

    op.alter_column(
        "task_history",
        "changed_by",
        nullable=False,
    )


    # ---------------------------------------------------------
    # 10. Remove old task columns
    # ---------------------------------------------------------
    op.drop_constraint(
        "tasks_owner_username_fkey",
        "tasks",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_tasks_owner_username",
        table_name="tasks",
    )

    op.drop_column(
        "tasks",
        "owner_username",
    )

    op.drop_column(
        "tasks",
        "completed",
    )


    # ---------------------------------------------------------
    # 11. Remove old history columns
    # ---------------------------------------------------------
    op.drop_column(
        "task_history",
        "action",
    )

    op.drop_column(
        "task_history",
        "description",
    )


def downgrade() -> None:
    # ---------------------------------------------------------
    # Restore old TASK columns
    # ---------------------------------------------------------
    op.add_column(
        "tasks",
        sa.Column(
            "owner_username",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "completed",
            sa.Boolean(),
            nullable=True,
        ),
    )

    # Restore username from user_id.
    op.execute(
        """
        UPDATE tasks
        SET owner_username = users.username
        FROM users
        WHERE tasks.user_id = users.id
        """
    )

    # Restore completed from status.
    op.execute(
        """
        UPDATE tasks
        SET completed = CASE
            WHEN status = 'completed' THEN TRUE
            ELSE FALSE
        END
        """
    )

    op.alter_column(
        "tasks",
        "owner_username",
        nullable=False,
    )

    op.alter_column(
        "tasks",
        "completed",
        nullable=False,
    )

    op.drop_constraint(
        "fk_tasks_user_id_users",
        "tasks",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_tasks_user_id",
        table_name="tasks",
    )

    op.drop_index(
        "ix_tasks_status",
        table_name="tasks",
    )

    op.create_index(
        "ix_tasks_owner_username",
        "tasks",
        ["owner_username"],
        unique=False,
    )

    op.create_foreign_key(
        "tasks_owner_username_fkey",
        "tasks",
        "users",
        ["owner_username"],
        ["username"],
    )

    op.drop_column("tasks", "updated_at")
    op.drop_column("tasks", "created_at")
    op.drop_column("tasks", "status")
    op.drop_column("tasks", "user_id")


    # ---------------------------------------------------------
    # Restore old TASK HISTORY columns
    # ---------------------------------------------------------
    op.add_column(
        "task_history",
        sa.Column(
            "action",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.add_column(
        "task_history",
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE task_history
        SET action = 'updated'
        WHERE action IS NULL
        """
    )

    op.alter_column(
        "task_history",
        "action",
        nullable=False,
    )

    op.drop_constraint(
        "fk_task_history_changed_by_users",
        "task_history",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_task_history_task_id_tasks",
        "task_history",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_task_history_changed_by",
        table_name="task_history",
    )

    op.create_foreign_key(
        "task_history_task_id_fkey",
        "task_history",
        "tasks",
        ["task_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.alter_column(
        "task_history",
        "task_id",
        nullable=True,
    )

    op.drop_column("task_history", "new_status")
    op.drop_column("task_history", "old_status")
    op.drop_column("task_history", "changed_by")


    # ---------------------------------------------------------
    # Restore USERS
    # ---------------------------------------------------------
    op.drop_column("users", "created_at")
    op.drop_column("users", "is_active")