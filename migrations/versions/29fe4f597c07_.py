"""empty message

Revision ID: 29fe4f597c07
Revises: 0fc22165700a
Create Date: 2022-11-07 11:16:14.528141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29fe4f597c07'
down_revision = '0fc22165700a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('menu_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('resto', sa.String(), nullable=True),
    sa.Column('meal', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('menu_id')
    )
    op.add_column('breakfast', sa.Column('menu_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'breakfast', 'menu', ['menu_id'], ['menu_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'breakfast', type_='foreignkey')
    op.drop_column('breakfast', 'menu_id')
    op.drop_table('menu')
    # ### end Alembic commands ###
