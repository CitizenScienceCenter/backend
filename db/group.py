from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Group(orm.Base):
    __tablename__ = 'groups'
    name = Column(String(100)) # TODO add alembic migration to remove unique
    description = Column(String(1000), unique=True)
    url =Column(String(200))
    owned_by = Column(UUID, ForeignKey('users.id'))
    api_key = Column(String(100))

