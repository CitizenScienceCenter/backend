from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm

class Task(orm.Base):
    __tablename__ = 'tasks'
    project_id = Column(String(100), ForeignKey('projects.id'))
    sequence = Column(Integer)
    media_path = Column(String(300))
    title = Column(String(300))
    content = Column(String(600))
