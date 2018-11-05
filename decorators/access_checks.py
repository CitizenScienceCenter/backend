from flask import session, request, g
from connexion import NoContent
from functools import wraps

from db import orm_handler, User

db_session = orm_handler.db_session

def ensure_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print('access check')
        if 'X-API-KEY' in request.headers:
            key = request.headers['X-API-KEY']
            user_key = db_session.query(User).filter(User.api_key == key).one_or_none()
            if user_key is not None:
                return func(*args, **kwargs)
            else:
                return NoContent, 401
        elif 'X-ANON' in request.headers:
            # TODO handle anonymous users (separate table?) and provide limited restrictions
            key = request.headers['X-ANON']
            return NoContent, 401
        else:
            return NoContent, 401
    return decorated_function

def ensure_model(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_function

def ensure_owner(func, model=None):
    def dec(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            print('access check')
            if 'X-API-KEY' in request.headers:
                key = request.headers['X-API-KEY']
                model_id = request.args['id']
                # TODO access request arguments and ensure it is owned by user
                query_field = model.user_id
                if model is Project or model is Group:
                    query_field = model.owned_by
                user = db_session.query(User).filter(User.api_key == key).one_or_none()
                obj = db_session.query(model).filter(query_field == user.id).filter(model.id == model_id).one_or_none()
                if user_key is not None:
                    if obj is not None:
                        return func(*args, **kwargs)
                    else:
                        return NoContent, 401        
                else:
                    return NoContent, 404
            else:
                return NoContent, 401
        return decorated_function
    return dec