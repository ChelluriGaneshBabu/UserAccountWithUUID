"""create User table

Revision ID: 8372c056bd4f
Revises: 5ea77b60c566
Create Date: 2023-05-25 11:01:59.697599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8372c056bd4f'
down_revision = '5ea77b60c566'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer()),
                    sa.Column("email_id",sa.Integer(),nullable=False),
                    sa.Column("first_name",sa.String(),nullable=False),
                    sa.Column("last_name",sa.String(),nullable=False),
                    sa.Column("phone_number",sa.BigInteger(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_on",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")),
                    sa.Column("modified_on",sa.DateTime),
                    sa.PrimaryKeyConstraint("id"),
                    sa.ForeignKeyConstraint(["email_id"],["emails.id"],ondelete="CASCADE")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
