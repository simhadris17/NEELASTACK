"""add tool ownership

Revision ID: 63deb2684921
Revises: c984937eb49f
Create Date: 2026-08-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "63deb2684921"
down_revision: Union[str, Sequence[str], None] = "c984937eb49f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tools",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    op.execute(
        "UPDATE tools SET user_id = 1 WHERE user_id IS NULL"
    )

    op.alter_column(
        "tools",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_index(
        "ix_tools_user_id",
        "tools",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_tools_user_id_users",
        "tools",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_tools_user_id_users",
        "tools",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_tools_user_id",
        table_name="tools",
    )

    op.drop_column("tools", "user_id")
