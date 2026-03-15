"""add license_expiry to company

Revision ID: d66acc9ac5a8
Revises: a11282491cf5
Create Date: 2026-03-10 11:00:08.327340

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd66acc9ac5a8'
down_revision = 'a11282491cf5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('license_expiry', sa.Date(), nullable=True))


def downgrade():
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_column('license_expiry')
