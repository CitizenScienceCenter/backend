from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Comment(orm.Base):
    __tablename__ = 'comments'
    source_id = Column(UUID)
    user_id = Column(UUID, ForeignKey('users.id'))
    parent = Column(UUID, ForeignKey('comments.id'), nullable=True)
    content = Column(JSONB)