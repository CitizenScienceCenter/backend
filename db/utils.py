from db.models import User
from flask import abort
from pony.flask import db_session
from pony.orm import *
import uuid


@db_session
def get_user(request, db):
    if 'X-API-KEY' in request.headers:
        key = uuid.UUID(request.headers["X-API-KEY"])
        try:
            return User.select(lambda u: u.api_key == key).first()
        except Exception:
            abort(404)
        
