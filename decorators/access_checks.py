import uuid
from functools import wraps
import prison
from db import Comment, Project, Submission, Task, User
from flask import abort, request
from pony.flask import db_session

db_tables = [
    "members",
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
    u = User.get(api_key=token)
    if u and (
        (u.info is not None and "anonymous" not in u.info) or u.anonymous == False
    ):
        return {str(u.id): token, "role": "user"}
    else:
        abort(401)


@db_session
def ensure_anon_key(token, required_scopes=None):
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
        self.model_id = None

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if "X-API-KEY" in request.headers:
                key = request.headers["X-API-KEY"]
                current = User.get(api_key=key)
                if not current:
                    abort(401)
                for key in kwargs.keys():
                    if "id" in key:
                        self.model_id = kwargs[key]
                requested = None
                if self.model is Project:
                    requested = Project.get(owner=current.id, id=self.model_id)
                elif self.model is User:
                    requested = current
                    if self.model_id is not None:
                        requested = User[self.model_id]
                    if requested is None or current != requested:
                        abort(401)
                elif self.model is Submission:
                    if self.model_id is not None:
                        requested = Submission.get(user_id=current.id, id=self.model_id)
                    else:
                        abort(404)
                elif self.model is Comment:
                    if self.model_id is not None:
                        requested = Comment.get(user_id=current.id, id=self.model_id)
                    else:
                        abort(404)
                elif self.model is Task:
                    if self.model_id is not None:
                        t = Task[self.model_id]
                        if (
                            t is not None
                            and t.activity_id.part_of.owned_by.id == current.id
                        ):
                            requested = t
                        else:
                            requested = None
                    else:
                        abort(404)
                if requested is None:
                    abort(401)
                else:
                    return func(*args, **kwargs)

        return decorated_function
