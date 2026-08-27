"""add tool type

Revision ID: 0a3aa1fbd861
Revises: 63deb2684921
Create Date: 2026-08-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0a3aa1fbd861"
down_revision: Union[str, Sequence[str], None] = "63deb2684921"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tools",
        sa.Column(
            "tool_type",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.execute(
        "UPDATE tools SET tool_type = 'generic' WHERE tool_type IS NULL"
    )

    op.alter_column(
        "tools",
        "tool_type",
        existing_type=sa.String(length=100),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column("tools", "tool_type")
