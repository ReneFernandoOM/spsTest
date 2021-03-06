"""empty message

Revision ID: d08e364598e6
Revises: 
Create Date: 2021-10-10 09:46:28.436935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd08e364598e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_block_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('api_user_id', sa.Integer(), nullable=False),
    sa.Column('revoked_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['api_user_id'], ['api_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token_block_list')
    # ### end Alembic commands ###
