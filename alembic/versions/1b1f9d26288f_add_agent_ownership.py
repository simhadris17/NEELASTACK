"""add agent ownership

Revision ID: 1b1f9d26288f
Revises: 09df5803cab1
Create Date: 2026-08-26 16:32:06.478558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1b1f9d26288f"
down_revision: Union[str, Sequence[str], None] = "09df5803cab1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Existing agents may already exist.
    # Add ownership temporarily as nullable.
    op.add_column(
        "agents",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    # Assign existing agents to the current existing user.
    op.execute(
        sa.text(
            "UPDATE agents SET user_id = 1 WHERE user_id IS NULL"
        )
    )

    op.create_index(
        "ix_agents_user_id",
        "agents",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_agents_user_id_users",
        "agents",
        "users",
        ["user_id"],
        ["id"],
    )

    # All agents must now have an owner.
    op.alter_column(
        "agents",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_agents_user_id_users",
        "agents",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_agents_user_id",
        table_name="agents",
    )

    op.drop_column(
        "agents",
        "user_id",
    )
