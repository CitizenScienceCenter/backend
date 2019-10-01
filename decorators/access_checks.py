from flask import request, abort
from functools import wraps
from db import User, Project, Activity, Submission, Comment
import prison
import uuid

from pony.flask import db_session

db_tables = [
    "activities",
    "users",
    "projects",
    "comments",
    "submissions",
    "media",
    "tasks",
]


@db_session
def ensure_key(token, required_scopes=None):
    """ 
    @todo Implement JWT authentication
    @body Using the `jose` lib, handle creation of JWTs for users (and renewal upon expiry)
    """
    token = uuid.UUID(token)
    u = User.get(api_key=token)
    if u is not None and ("anonymous" not in u.info or u.anonymous == False):
        return {str(u.id): token, "role": "user"}
    else:
        abort(401)


@db_session
def ensure_anon_key(token, required_scopes=None):
    token = uuid.UUID(token)
    u = User.get(api_key=token)
    if u is not None and u.anonymous is True:
        # TODO check on sub roles for Connexion
        return {"anonymous": token, "role": "anonymous"}
    else:
        abort(401)


@db_session
class ensure_model(object):
    def __init__(self, model):
        self.model = model

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if "search_term" in request.args:
                search = prison.loads(request.args["search_term"])
                allowed_table = True
                for t in search["select"]["tables"]:
                    if t.lower().split(" ")[0] not in db_tables:
                        allowed_table = False
                        break
                if not allowed_table:
                    abort(401)
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return decorated_function


@db_session
class ensure_owner(object):
    def __init__(self, model):
        self.model = model

    @db_session
    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if "X-API-KEY" in request.headers:
                key = request.headers["X-API-KEY"]
                key = uuid.UUID(key)
                current = User.get(api_key=key)
                if not current:
                    abort(401)
                model_id = request.view_args["id"]
                model = self.model
                requested = None
                if model is Project:
                    requested = Project.get(owned_by=current.id, id=model_id)
                elif model is Activity:
                    for p in current.owned_projects:
                        for a in p.activities:
                            if str(a.id) == model_id:
                                return func(*args, **kwargs)
                    abort(404)
                elif model is User:
                    key = uuid.UUID(key)
                    requested = User.get(id=model_id)
                    if requested is None or current != requested:
                        abort(401)
                elif model is Submission:
                    requested = Submission.get(user_id=current.id, id=model_id)
                elif model is Comment:
                    requested = Comment.get(user_id=current.id, id=model_id)
                if requested is None:
                    abort(401)
                else:
                    return func(*args, **kwargs)

        return decorated_function
