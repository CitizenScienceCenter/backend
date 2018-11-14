"""create comments table

Revision ID: c88d834c7e1b
Revises: 
Create Date: 2018-10-11 12:28:09.005968

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'c88d834c7e1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
        'comments',
        sa.Column('id', UUID, primary_key=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow()),
        sa.Column('source_id', UUID),
        sa.Column('content', JSONB(), nullable=False),
        sa.Column('parent', UUID, nullable=True),
    )


def downgrade():
    op.drop_table('comments')
