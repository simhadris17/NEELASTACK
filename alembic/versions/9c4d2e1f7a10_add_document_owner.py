"""Add document ownership for private files."""

from alembic import op
import sqlalchemy as sa

revision = "9c4d2e1f7a10"
down_revision = "f8ed3b59863a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("documents")}
    if "user_id" not in columns:
        op.add_column("documents", sa.Column("user_id", sa.Integer(), nullable=True))
    indexes = {index["name"] for index in sa.inspect(bind).get_indexes("documents")}
    if "ix_documents_user_id" not in indexes:
        op.create_index("ix_documents_user_id", "documents", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_documents_user_id", table_name="documents")
    op.drop_column("documents", "user_id")
