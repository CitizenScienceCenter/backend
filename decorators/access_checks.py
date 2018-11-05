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

def ensure_owner(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print('access check')
        if 'X-API-KEY' in request.headers:
            key = request.headers['X-API-KEY']
            # TODO access request arguments and ensure it is owned by user
            user_key = db_session.query(User).filter(User.api_key == key).one_or_none()
            if user_key is not None:
                return func(*args, **kwargs)
            else:
                return NoContent, 401
        else:
            return NoContent, 401
    return decorated_function