"""add queue scheduling and retry metadata"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e7a1f2b3c4d5"
down_revision: Union[str, Sequence[str], None] = "d4f2a1c9e8b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("jobs", sa.Column("available_at", sa.DateTime(), nullable=True))
    op.add_column("jobs", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.add_column("jobs", sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("jobs", sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"))
    op.add_column("jobs", sa.Column("progress", sa.Integer(), nullable=False, server_default="0"))
    op.execute("UPDATE jobs SET available_at = created_at WHERE available_at IS NULL")
    op.execute("UPDATE jobs SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column("jobs", "available_at", nullable=False)
    op.alter_column("jobs", "updated_at", nullable=False)
    op.create_index("ix_jobs_available_at", "jobs", ["available_at"])


def downgrade() -> None:
    op.drop_index("ix_jobs_available_at", table_name="jobs")
    for column in ("progress", "max_attempts", "attempts", "updated_at", "available_at"):
        op.drop_column("jobs", column)
