from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm


class User(orm.Base):
    __tablename__ = 'users'
    user_id = Column(String(100), primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    pwd = Column(String(100))
    api_key = Column(String(100))
    confirmed = Column(Boolean)

