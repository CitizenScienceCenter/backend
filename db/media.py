from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import db.orm_handler as orm

class Media(orm.Base):
    __tablename__ = 'media'
    source_id = Column(UUID, nullable=True)
    path = Column(String(800))
    name = Column(String(400))
    filetype = Column(String(400))

    def __init__(self, source_id, path, name, f_type):
        self.source_id = source_id
        self.path = path
        self.name = name
        self.filetype = f_type
    
