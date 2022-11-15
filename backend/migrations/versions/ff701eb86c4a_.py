"""empty message

Revision ID: ff701eb86c4a
Revises: 460db3b81808
Create Date: 2022-11-14 15:54:13.199865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff701eb86c4a'
down_revision = '460db3b81808'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('RefreshToken',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('refresh_token_value', sa.String(length=512), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('refresh_token_value')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('RefreshToken')
    # ### end Alembic commands ###