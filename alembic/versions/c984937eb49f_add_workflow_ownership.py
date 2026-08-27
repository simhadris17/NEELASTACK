"""add workflow ownership

Revision ID: c984937eb49f
Revises: 1b1f9d26288f
Create Date: 2026-08-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c984937eb49f"
down_revision: Union[str, Sequence[str], None] = "1b1f9d26288f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "workflows",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    op.execute(
        "UPDATE workflows SET user_id = 1 WHERE user_id IS NULL"
    )

    op.alter_column(
        "workflows",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_index(
        "ix_workflows_user_id",
        "workflows",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_workflows_user_id_users",
        "workflows",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_workflows_user_id_users",
        "workflows",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_workflows_user_id",
        table_name="workflows",
    )
    op.drop_column("workflows", "user_id")
