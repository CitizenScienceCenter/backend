from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    create_engine,
    JSON,
    ForeignKey,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
import db.orm_handler as orm
from sqlalchemy.dialects.postgresql import UUID


class Activity(orm.Base):
    __tablename__ = "activities"
    name = Column(String(100))
    description = Column(String(1000))
    platform = Column(String(50), nullable=False, default="Both")
    active = Column(Boolean, default=False)
    part_of = Column(UUID, ForeignKey("projects.id"))
