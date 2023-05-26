"""create Profile table

Revision ID: 43982152f032
Revises: 480d307b291f
Create Date: 2023-05-25 11:23:17.422070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43982152f032'
down_revision = '480d307b291f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("profiles",
                    sa.Column("id",sa.Integer()),
                    sa.Column("date_of_birth",sa.Date()),
                    sa.Column("address",sa.String()),
                    sa.Column("highest_qualification",sa.String()),
                    sa.Column("user_id",sa.Integer(),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.ForeignKeyConstraint(["user_id"],["users.id"],ondelete="CASCADE")
                    )
    pass


def downgrade() -> None:
    op.drop_table("profiles")
    pass
