from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm

class Project(orm.Base):
    __tablename__ = 'projects'
    project_id = Column(String(100), primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    owned_by = Column(String(100), ForeignKey('users.user_id'))