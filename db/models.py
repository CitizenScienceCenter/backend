import uuid
from datetime import datetime
from pony.orm import Set, PrimaryKey, Optional, Required, Json, Database


DB = Database()

def gen_api_key():
    return str(uuid.uuid4())

class User(DB.Entity):
    _table_ = "users"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    username = Required(str, unique=True)
    email = Optional(str, unique=True)
    anonymous = Optional(bool, default=False)
    pwd = Required(str)
    api_key = Required(str, default=gen_api_key)
    confirmed = Required(bool, default=False)
    owned_projects = Set("Project")
    member_of = Set("Member")
    submissions = Set("Submission")
    tokens = Set("OToken")
    comments = Set("Comment")


class OToken(DB.Entity):
    _table_ = "oauth_tokens"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    owner = Required(User)
    token = Required(uuid.UUID, default=uuid.uuid4)
    expiry = Optional(datetime)

class Member(DB.Entity):
    _table_ = "members"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    user_id = Required("User", reverse="member_of")
    project_id = Required("Project", reverse="members")
    role = Required("Role")

class Role(DB.Entity):
    _table_ = "roles"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    name = Required(str)
    view_project = Required(bool, default=False)
    edit_project = Required(bool, default=False)
    delete_project = Required(bool, default=False)
    view_tasks = Required(bool, default=False)
    edit_tasks = Required(bool, default=False)
    add_tasks = Required(bool, default=False)
    delete_tasks = Required(bool, default=False)
    edit_media = Required(bool, default=False)
    delete_media = Required(bool, default=False)
    view_submissions = Required(bool, default=False)
    edit_submissions = Required(bool, default=False)
    delete_submissions = Required(bool, default=False)
    export_data = Required(bool, default=False)
    members = Set("Member")

class ProjectGroup(DB.Entity):
    _table_ = "projectgroups"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    name = Required(str)
    owner = Required(str)
    projects = Set("Project")
    members = Set("Member")

class Project(DB.Entity):
    _table_ = "projects"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    name = Required(str)
    anonymous_allowed = Optional(bool, default=True)
    description = Required(str)
    platform = Required(str)
    active = Required(bool, default=False)
    owner = Required("User", reverse="owned_projects")
    members = Set("Member")
    media = Set("Media")
    tasks = Set("Task")


class Task(DB.Entity):
    _table_ = "tasks"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    part_of = Required(Project)
    sequence = Optional(int)
    title = Required(str)
    required = Required(bool, default=True)
    allow_multiple = Required(bool, default=True)
    content = Optional(Json)
    media = Set("Media")
    submissions = Set("Submission")

class Submission(DB.Entity):
    _table_ = "submissions"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    task_id = Required(Task)
    draft = Optional(bool, default=False)
    user_id = Required(User)
    response = Required(Json)
    media = Set("Media")

class Comment(DB.Entity):
    _table_ = "comments"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    source_id = Required(uuid.UUID)
    parent = Optional("Comment")
    children = Set("Comment")
    text = Required(str)
    user_id = Required(User)

class Media(DB.Entity):
    _table_ = "media"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Optional(datetime, default=datetime.now)
    info = Required(Json, default={})
    source_id = Required(uuid.UUID)
    path = Required(str)
    name = Required(str)
    filetype = Optional(str)
    project = Optional(Project)
    submission = Optional(Submission)
    task = Optional(Task)
