"""create Verify Token table

Revision ID: 5ea77b60c566
Revises: 1e26d261cea1
Create Date: 2023-05-25 11:00:45.906181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ea77b60c566'
down_revision = '1e26d261cea1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("verify_tokens",
                    sa.Column("id",sa.Integer()),
                    sa.Column("email_id",sa.Integer(),nullable=False),
                    sa.Column("token",sa.String()),
                    sa.PrimaryKeyConstraint("id"),
                    sa.ForeignKeyConstraint(["email_id"],["emails.id"],ondelete= "CASCADE")
                    )
    pass


def downgrade() -> None:
    op.drop_table("verify_tokens")
    pass
