"""add tool config

Revision ID: 15c7b2743b03
Revises: 0a3aa1fbd861
Create Date: 2026-08-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "15c7b2743b03"
down_revision: Union[str, Sequence[str], None] = "0a3aa1fbd861"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tools",
        sa.Column(
            "config",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.execute(
        "UPDATE tools SET config = '{}' WHERE config IS NULL"
    )

    op.alter_column(
        "tools",
        "config",
        existing_type=sa.JSON(),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column("tools", "config")
