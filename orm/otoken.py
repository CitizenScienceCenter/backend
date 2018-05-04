from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import orm.orm_handler as orm

Base = declarative_base()

class OToken(Base):
    __tablename__ = 'oauth_tokens'
    token_id = Column(String(100), primary_key=True)
    user_id = Column(String(100), ForeignKey('users.user_id'))
    created_at = Column(DateTime(), default=orm._get_date)
