from flask import session, request, g
from connexion import NoContent
from functools import wraps

from db import orm_handler, User

db_session = orm_handler.init_db()

def ensure_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print('access check')
        try:
            # _, access_token = request.headers['Authorization'].split()
            key = request.headers['X-API-KEY']
        except:
            key = ''
        # TODO add check for oauth tokens
        print(key)
        user_key = db_session.query(User).filter(User.api_key == key).one_or_none()
        if user_key is not None:
            return func(*args, **kwargs)
        else:
            return NoContent, 401
    return decorated_function
