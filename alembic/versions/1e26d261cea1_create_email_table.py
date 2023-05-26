"""create email table

Revision ID: 1e26d261cea1
Revises: 
Create Date: 2023-05-25 10:34:46.091107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e26d261cea1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("emails",
                    sa.Column("id",sa.Integer()),
                    sa.Column("user_email",sa.String(),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("user_email"))
    pass


def downgrade() -> None:
    op.drop_table("emails")
    pass
