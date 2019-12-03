import uuid
from functools import wraps

from db import Comment, Project, Submission, Task, User
from flask import abort, request
from pony.flask import db_session


@db_session
class multiple_submissions:
    def __init__(self, func):
        pass

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            key = request.headers["X-API-KEY"]
            u = User.get(api_key=key)
            if u is None:
                abort(404)
            task_id = request.view_args["id"]
            t = Task.get(id=task_id)
            if t is None:
                abort(404)
            if t.submissions.filter(user_id=u.id).count() >= 1 and t.allow_multiple == False:
                abort(403, 'Multiple submissions not allowed')
            else:
                return func(*args, **kwargs)

        return decorated_function
