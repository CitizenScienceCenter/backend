from flask import session, request, g, abort
from connexion import NoContent
from functools import wraps
from db import *
import prison
import uuid

db_tables = ['activities', 'users', 'projects', 'comments', 'submissions', 'media', 'tasks']


@db_session
def ensure_key(token, required_scopes=None):
    u = User.get(api_key=token)
    if u is not None:
        return {'sub': 'admin'}
    else:
        abort(401)

@db_session
def ensure_anon_key(token, required_scopes=None):
    return ensure_key(token, required_scopes)

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
                print(allowed_table)
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
            print("owner access check")
            if "X-API-KEY" in request.headers:
                key = request.headers["X-API-KEY"]
                current = User.get(api_key=key)
                if not current:
                    abort(401)
                model_id = request.view_args["id"]
                model = self.model
                owned_id = None
                requested = None
                if model is Project:
                    requested = Project.get(owned_by=current.id, id=model_id)
                elif model is Activity:
                    found = False                 
                    for p in current.owned_projects:
                        for a in p.activities:
                            if str(a.id) == model_id:
                                print("FOUND")
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
