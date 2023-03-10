"""change type data to String  in Product.kode_produk

Revision ID: 8d73767a6ad2
Revises: cc3df10252d9
Create Date: 2023-01-31 12:55:51.203739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d73767a6ad2'
down_revision = 'cc3df10252d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_produk', schema=None) as batch_op:
        batch_op.alter_column('kode_produk',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_produk', schema=None) as batch_op:
        batch_op.alter_column('kode_produk',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
