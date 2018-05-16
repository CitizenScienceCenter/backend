from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm

class Submission(orm.Base):
    __tablename__ = 'submissions'
    task_id = Column(String(100), ForeignKey('tasks.id'))
    user_id = Column(String(100), ForeignKey('users.id'))
    content = Column(JSON())
    media_path = Column(String(1000))

    def create(self):
        self.created_at = _get_date

    def update(self):
        self.updated_at = updated_at

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])