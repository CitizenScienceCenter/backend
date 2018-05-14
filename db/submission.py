from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm

class Submission(orm.Base):
    __tablename__ = 'submissions'
    sub_id = Column(String(100), primary_key=True)
    task_id = Column(String(100), ForeignKey('tasks.task_id'))
    user_id = Column(String(100), ForeignKey('users.user_id'))
    content = Column(JSON())
    media_path = Column(String(1000))
    created_at = Column(DateTime(), default=orm._get_date)
    updated_at = Column(DateTime(), onupdate=orm._get_date)

    def create(self):
        self.created_at = _get_date

    def update(self):
        self.updated_at = updated_at

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])