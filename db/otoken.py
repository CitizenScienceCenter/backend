from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import db.orm_handler as orm

class OToken(orm.Base):
    __tablename__ = 'oauth_tokens'
    user_id = Column(UUID, ForeignKey('users.id'))
    project_id = Column(UUID, ForeignKey('projects.id'))