from flask import session, request
from connexion import NoContent
from functools import wraps

def ensure_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['user']:
            if request.headers.get('x-api-key') and request.headers.get('x-api-key') == session['user']['api_key']:
                return func(*args, **kwargs)
            else:
                return NoContent, 401
        else:
            return NoContent, 401
    return decorated_function
