"""empty message

Revision ID: a11282491cf5
Revises: 7f3293fab449
Create Date: 2022-11-11 11:11:24.836577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a11282491cf5'
down_revision = '7f3293fab449'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.alter_column('companyname',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('company_address',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('company_address_number',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=5),
               existing_nullable=False)
        batch_op.alter_column('company_city',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('company_site',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('company_phone',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=20),
               existing_nullable=False)

    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.alter_column('service',
               existing_type=sa.VARCHAR(length=300),
               type_=sa.String(length=400),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.alter_column('service',
               existing_type=sa.String(length=400),
               type_=sa.VARCHAR(length=300),
               existing_nullable=True)

    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.alter_column('company_phone',
               existing_type=sa.String(length=20),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.alter_column('company_site',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('company_city',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('company_address_number',
               existing_type=sa.String(length=5),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.alter_column('company_address',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('companyname',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###
