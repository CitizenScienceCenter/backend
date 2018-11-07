from flask import session, request, g
from connexion import NoContent
from functools import wraps
from db import *
import prison

db_session = orm_handler.db_session
db_tables = orm_handler.Base.metadata.tables.keys()


def ensure_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print("access check")
        if "X-API-KEY" in request.headers:
            key = request.headers["X-API-KEY"]
            user_key = db_session.query(User).filter(User.api_key == key).one_or_none()
            if user_key is not None:
                return func(*args, **kwargs)
            else:
                return NoContent, 401
        elif "X-ANON" in request.headers:
            # TODO handle anonymous users (separate table?) and provide limited restrictions
            key = request.headers["X-ANON"]
            return NoContent, 401
        else:
            return NoContent, 401

    return decorated_function


def ensure_model(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "search_term" in request.args:
            search = prison.loads(request.args["search_term"])
            allowed_table = True
            for t in search["select"]["tables"]:
                if t.lower() not in db_tables:
                    allowed_table = False
                    break
            print(allowed_table)
            if not allowed_table:
                return NoContent, 401
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
                if model is Group:
                    query_field = model.owned_by
                    user = (
                        db_session.query(User)
                        .filter(User.api_key == key)
                        .filter(User.member_of.any(id=model_id))
                        .one_or_none()
                    )
                    if user is None:
                        return NoContent, 401
                    owned_id = user.id
                elif model is Project:
                    query_field = model.owned_by
                    project = (
                        db_session.query(model)
                        .filter(model.id == model_id)
                        .one_or_none()
                    )
                    if project is not None:
                        print(project.owned_by)
                        account = db_session.query(User).all()
                        print(account)
                        if account:
                            owned_id = project.owned_by
                        else:
                            return NoContent, 401
                    else:
                        return NoContent, 404
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
                        return NoContent, 401
                else:
                    return NoContent, 401
            else:
                return NoContent, 401

        return decorated_function
