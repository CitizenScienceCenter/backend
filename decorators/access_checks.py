from flask import session, request, g, abort
from connexion import NoContent
from functools import wraps
from db import *
import prison

db_session = orm_handler.db_session()
db_tables = orm_handler.Base.metadata.tables.keys()


def ensure_key(token, required_scopes=None):
        key = token
        user_key = db_session.query(User).filter(User.api_key == key).one_or_none()
        db_session.close()
        if user_key is not None:
            return dict(sub=user_key.username)
        else:
            return None

def ensure_anon_key(token, required_scopes=None):
    return ensure_key(token, required_scopes)

def ensure_model(func):
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


class ensure_owner(object):
    def __init__(self, model):
        self.model = model

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            print("owner access check")
            if "X-API-KEY" in request.headers:
                key = request.headers["X-API-KEY"]
                model_id = request.view_args["id"]
                model = self.model
                query_field = None
                owned_id = None
                if model is Project:
                    query_field = model.owned_by
                    owner = (
                        db_session.query(User)
                        .filter(User.api_key == key)
                        .filter(User.member_of.any(id=model_id))
                        .one_or_none()
                    )
                    if owner is None:
                        abort(401)
                    owned_id = owner.id
                elif model is Activity:
                    return func(*args, **kwargs)
                    # query_field = model.part_of
                    # act = (
                    #     db_session.query(model)
                    #     .filter(model.id == model_id)
                    #     .one_or_none()
                    # )
                    # if act is not None:
                    #     print(project.owned_by)
                    #     account = db_session.query(User).all()
                    #     print(account)
                    #     if account:
                    #         owned_id = project.owned_by
                    #     else:
                    #         return NoContent, 401
                    # else:
                    #     return NoContent, 404
                elif model is User:
                    query_field = model.id
                    owner = db_session.query(User).filter(User.api_key == key).one_or_none()
                    if owner is None:
                        abort(404)
                    owned_id = owner.id
                else:
                    query_field = model.user_id
                if owned_id is not None:
                    obj = (
                        db_session.query(model)
                        .filter(query_field == owned_id)
                        .filter(model.id == model_id)
                        .one_or_none()
                    )
                    if obj is not None:
                        return func(*args, **kwargs)
                    else:
                        abort(401)
                else:
                    abort(401)
            else:
                abort(401)

        return decorated_function
