from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import orm.orm_handler as orm

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String(100), primary_key=True)
    username = Column(String(100))
    email = Column(String(100))
    pwd = Column(String(100))
    api_key = Column(String(100))
    created_at = Column(DateTime(), default=orm._get_date)
    updated_at = Column(DateTime(), onupdate=orm._get_date)

