"""empty message

Revision ID: b227061b5562
Revises: fdb953976ffb
Create Date: 2021-05-02 08:34:19.136533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b227061b5562'
down_revision = 'fdb953976ffb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lianjia_village_data_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.String(length=128), nullable=False),
    sa.Column('month', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lianjia_village_data_info')
    # ### end Alembic commands ###
