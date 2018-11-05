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
from sqlalchemy.orm import scoped_session, sessionmaker
import db.orm_handler as orm
from sqlalchemy.dialects.postgresql import UUID, JSONB


class Submission(orm.Base):
    __tablename__ = "submissions"
    task_id = Column(UUID, ForeignKey("tasks.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    draft = Column(Boolean, default=False)
    content = Column(JSONB)

    def create(self):
        self.created_at = _get_date

    def update(self):
        self.updated_at = updated_at

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith("_")])
