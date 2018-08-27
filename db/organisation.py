from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm
from sqlalchemy.dialects.postgresql import UUID

class Organistaion(orm.Base):
    __tablename__ = 'orgs'
    name = Column(String(100), unique=True)
    description = Column(String(100), unique=True)
    created_by = Column(UUID, ForeignKey('users.id'))
    api_key = Column(String(100))

