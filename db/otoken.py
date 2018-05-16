from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm

class OToken(orm.Base):
    __tablename__ = 'oauth_tokens'
    token_id = Column(String(100), primary_key=True)
    user_id = Column(String(100), ForeignKey('users.user_id'))
    user_id = Column(String(100), ForeignKey('projects.project_id'))