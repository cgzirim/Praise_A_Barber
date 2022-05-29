"""empty message

Revision ID: 5fe6819e26aa
Revises: f2287ac22d91
Create Date: 2022-05-29 19:54:26.234604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fe6819e26aa'
down_revision = 'f2287ac22d91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('barber_styles_style_id_fkey', 'barber_styles', type_='foreignkey')
    op.create_foreign_key(None, 'barber_styles', 'style', ['style_id'], ['ids'])
    op.alter_column('style', 'ids',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.drop_column('style', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('style', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('style_id_seq'::regclass)"), autoincrement=True, nullable=False))
    op.alter_column('style', 'ids',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    op.drop_constraint(None, 'barber_styles', type_='foreignkey')
    op.create_foreign_key('barber_styles_style_id_fkey', 'barber_styles', 'style', ['style_id'], ['id'])
    # ### end Alembic commands ###
