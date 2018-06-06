from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm

class Task(orm.Base):
    __tablename__ = 'tasks'
    project_id = Column(String(100), ForeignKey('projects.id'))
    sequence = Column(Integer)
    title = Column(String(300))
    required = Column(Boolean, default=True)
    content = Column(JSON())
