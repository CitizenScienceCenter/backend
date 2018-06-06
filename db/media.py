from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm

class Media(orm.Base):
    __tablename__ = 'media'
    source_id = Column(String(200), nullable=False)
    path = Column(String(400))

    def __init__(self, source_id, path):
        self.source_id = source_id
        self.path = path
    