import uuid
from functools import wraps

from db import Comment, Project, Submission, Task, User
from flask import abort, request
from pony.flask import db_session

@db_session
def get_user_groups(request):
    return User.get(api_key=request.headers['X-API-KEY']).member_of

@db_session
def ensure_task_access(*args, **kwargs):
    def inner(func):
        task = Task.get(id=kwargs['tid'])
        proj = task.part_of
    return inner

@db_session
def ensure_group_access(*args, **kwargs):
    def inner(func):
        if 'X-API-KEY' in request.headers:
            current = User.get(api_key=request.headers['X-API-KEY'])
            if not current:
                abort(404, "User not found")
            else:
                member_of = current.member_of
                model = kwargs['model']
                action = kwargs['action']
                sid = kwargs['id']
                source = ProjectGroup.get(id=sid)
                if source is None:
                    source = Project.get(id=sid)
                    if source is None:
                        abort(404)
                m = source.members.filter(lambda m : m.user_id == current.id)
                if m.role[action]:
                    return func(*args, **kwargs)
                else:
                    abort(401)
    return inner
