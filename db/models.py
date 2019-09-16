import uuid
from pony.orm import *
from datetime import datetime

db = Database()


class User(db.Entity):
    _table_ = 'users'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    pwd = Required(str)
    api_key = Required(uuid.UUID, default=uuid.uuid4)
    confirmed = Required(bool, default=False)
    projects = Set('Project')
    owned_projects = Set('Project')
    submissions = Set('Submission')
    tokens = Set('OToken')
    comments = Set('Comment')

class OToken(db.Entity):
    _table_ = 'oauth_tokens'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    owner = Required(User)
    part_of = Required('Project')    
    token = Required(uuid.UUID, default=uuid.uuid4)
    expiry = Optional(datetime)

class Project(db.Entity):
    _table_ = 'projects'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    name = Required(str)
    description = Required(str)
    active = Required(bool, default=False)
    activities = Set('Activity')
    owned_by = Required(User, reverse='owned_projects')
    members = Set(User)
    media = Set('Media')
    tokens = Set(OToken)

class Activity(db.Entity):
    _table_ = 'activities'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    name = Required(str)
    description = Required(str)
    platform = Required(str)
    active = Required(bool, default=False)
    part_of = Required('Project')
    media = Set('Media')
    tasks = Set('Task')

class Task(db.Entity):
    _table_ = 'tasks'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    activity_id = Required(Activity)
    sequence = Optional(int)
    title = Required(str)
    required = Required(bool, default=True)
    allow_multiple = Required(bool, default=True)
    content = Optional(Json)
    media = Set('Media')
    submissions = Set('Submission')

class Submission(db.Entity):
    _table_ = 'submissions'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    task_id = Required(Task)
    draft = Optional(bool, default=False)
    user_id = Required(User)
    response = Required(Json)
    media = Set('Media')

class Comment(db.Entity):
    _table_ = 'comments'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    source_id = Required(uuid.UUID)
    parent = Optional('Comment')
    children = Set('Comment')
    text = Required(str)
    user_id = Required(User)

class Media(db.Entity):
    _table_ = 'media'
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)
    info = Required(Json, default={})
    media_source_id = Required(uuid.UUID)
    path = Required(str)
    name = Required(str)
    filetype = Optional(str)
    project = Optional(Project)
    submission = Optional(Submission)
    activity = Optional(Activity)
    task = Optional(Task)
    submission = Required(Submission)
