"""add project ownership

Revision ID: 09df5803cab1
Revises: f8ed3b59863a
Create Date: 2026-08-26 16:25:38.655505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "09df5803cab1"
down_revision: Union[str, Sequence[str], None] = "f8ed3b59863a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Existing projects already exist, so add user_id temporarily as nullable.
    op.add_column(
        "projects",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    # Assign existing projects to the current existing user.
    # Current database has user id=1.
    op.execute(
        sa.text(
            "UPDATE projects SET user_id = 1 WHERE user_id IS NULL"
        )
    )

    op.create_index(
        "ix_projects_user_id",
        "projects",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_projects_user_id_users",
        "projects",
        "users",
        ["user_id"],
        ["id"],
    )

    # From this point every project must have an owner.
    op.alter_column(
        "projects",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_projects_user_id_users",
        "projects",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_projects_user_id",
        table_name="projects",
    )

    op.drop_column(
        "projects",
        "user_id",
    )
