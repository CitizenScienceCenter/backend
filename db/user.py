from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
import db.orm_handler as orm
from sqlalchemy.dialects.postgresql import UUID

orgs_users = Table('user_organisations', orm.Base.metadata,
    Column('org_id', UUID, ForeignKey('orgs.id')),
    Column('user_id', UUID, ForeignKey('users.id'))
)

class User(orm.Base):
    __tablename__ = 'users'
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    pwd = Column(String(100))
    api_key = Column(String(100))
    confirmed = Column(Boolean)
    member_of = relationship('org_user', secondary=orgs_users)

