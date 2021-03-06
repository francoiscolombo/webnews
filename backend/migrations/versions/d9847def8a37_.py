"""empty message

Revision ID: d9847def8a37
Revises: 
Create Date: 2020-03-27 16:16:35.621863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9847def8a37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('application', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_auth_application'), 'auth', ['application'], unique=True)
    op.create_table('weather',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=15), nullable=True),
    sa.Column('country', sa.String(length=80), nullable=True),
    sa.Column('flag', sa.String(length=512), nullable=True),
    sa.Column('town', sa.String(length=80), nullable=True),
    sa.Column('tendency', sa.String(length=80), nullable=True),
    sa.Column('wind_speed', sa.String(length=20), nullable=True),
    sa.Column('temperature_min', sa.String(length=20), nullable=True),
    sa.Column('temperature_max', sa.String(length=20), nullable=True),
    sa.Column('temperature', sa.String(length=20), nullable=True),
    sa.Column('humidity', sa.String(length=40), nullable=True),
    sa.Column('clouds', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_weather_ip'), 'weather', ['ip'], unique=True)
    op.create_table('web_news_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_web_news_category_name'), 'web_news_category', ['name'], unique=True)
    op.create_table('web_news_keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_web_news_keyword_tag'), 'web_news_keyword', ['tag'], unique=True)
    op.create_table('web_news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('author', sa.String(length=64), nullable=True),
    sa.Column('photo', sa.String(length=256), nullable=True),
    sa.Column('source', sa.String(length=256), nullable=True),
    sa.Column('is_headline', sa.String(length=3), nullable=True),
    sa.Column('is_top_story', sa.String(length=3), nullable=True),
    sa.Column('date_publish', sa.DateTime(), nullable=True),
    sa.Column('content', sa.String(length=2048), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['web_news_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_web_news_author'), 'web_news', ['author'], unique=False)
    op.create_index(op.f('ix_web_news_title'), 'web_news', ['title'], unique=True)
    op.create_table('link',
    sa.Column('web_news_id', sa.Integer(), nullable=False),
    sa.Column('web_news_keyword_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['web_news_id'], ['web_news.id'], ),
    sa.ForeignKeyConstraint(['web_news_keyword_id'], ['web_news_keyword.id'], ),
    sa.PrimaryKeyConstraint('web_news_id', 'web_news_keyword_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link')
    op.drop_index(op.f('ix_web_news_title'), table_name='web_news')
    op.drop_index(op.f('ix_web_news_author'), table_name='web_news')
    op.drop_table('web_news')
    op.drop_index(op.f('ix_web_news_keyword_tag'), table_name='web_news_keyword')
    op.drop_table('web_news_keyword')
    op.drop_index(op.f('ix_web_news_category_name'), table_name='web_news_category')
    op.drop_table('web_news_category')
    op.drop_index(op.f('ix_weather_ip'), table_name='weather')
    op.drop_table('weather')
    op.drop_index(op.f('ix_auth_application'), table_name='auth')
    op.drop_table('auth')
    # ### end Alembic commands ###
