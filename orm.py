from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import datetime

Base = declarative_base()

def _get_date():
    return datetime.datetime.now()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String(100), primary_key=True)
    username = Column(String(100))
    email = Column(String(100))
    pwd = Column(String(100))
    api_key = Column(String(100))
    created_at = Column(DateTime(), default=_get_date)
    updated_at = Column(DateTime(), onupdate=_get_date)

class OToken(Base):
    __tablename__ = 'oauth_tokens'
    token_id = Column(String(100), primary_key=True)
    user_id = Column(String(100), ForeignKey('users.user_id'))
    created_at = Column(DateTime(), default=_get_date)

class Project(Base):
    __tablename__ = 'projects'
    proj_id = Column(String(100), primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    owned_by = Column(String(100), ForeignKey('users.user_id'))
    created_at = Column(DateTime(), default=_get_date)
    updated_at = Column(DateTime(), onupdate=_get_date)

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(String(100), primary_key=True)
    project_id = Column(String(100), ForeignKey('projects.proj_id'))
    sequence = Column(Integer)
    content = Column(String(600))
    

class Submission(Base):
    __tablename__ = 'submissions'
    sub_id = Column(String(100), primary_key=True)
    task_id = Column(String(100), ForeignKey('tasks.task_id'))
    content = Column(JSON())
    media_path = Column(String(1000))
    created_at = Column(DateTime(), default=_get_date)
    updated_at = Column(DateTime(), onupdate=_get_date)

class Participant(Base):
    __tablename__ = 'participants'
    part_id = Column(String(100), primary_key=True)
    proj_id = Column(String(100), ForeignKey('projects.proj_id'))
    user_id = Column(String(100), ForeignKey('users.user_id'))
    created_at = Column(DateTime(), default=_get_date)

    def create(self):
        self.created_at = _get_date

    def update(self):
        self.updated_at = updated_at

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.drop_all(engine) 
    Base.metadata.create_all(bind=engine)
    return db_session
