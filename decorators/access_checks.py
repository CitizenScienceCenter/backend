from flask import session, request, g
from connexion import NoContent
from functools import wraps

import orm

db_session = orm.init_db('postgresql://pybossa:tester@localhost/cccs')

def ensure_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print('access check')
        try:
            _, access_token = request.headers['Authorization'].split()
        except:
            access_token = ''
        user_key = db_session.query(orm.User).filter(orm.User.api_key == access_token).one_or_none()
        if key == user_key:
            return func(*args, **kwargs)
        else:
            return NoContent, 401
    return decorated_function
