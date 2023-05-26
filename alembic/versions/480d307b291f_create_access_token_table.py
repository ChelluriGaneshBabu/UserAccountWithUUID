"""create access token table

Revision ID: 480d307b291f
Revises: 8372c056bd4f
Create Date: 2023-05-25 11:12:05.403016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '480d307b291f'
down_revision = '8372c056bd4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("accesstokens",
                    sa.Column("id",sa.Integer(),nullable=False),
                    sa.Column("access_token",sa.String(),nullable=False),
                    sa.Column("expire_time",sa.TIMESTAMP(),nullable=False),
                    sa.Column("user_id",sa.Integer(),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.ForeignKeyConstraint(["user_id"],["users.id"],ondelete="CASCADE")
                    )
    pass


def downgrade() -> None:
    op.drop_table("accesstokens")
    pass
