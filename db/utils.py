from db.models import User
from flask import abort
from pony.flask import db_session
from pony.orm import *
import uuid


@db_session
def get_user(request, db):
    if "X-API-KEY" in request.headers:
        key = request.headers["X-API-KEY"]
        u = User.get(api_key=key)
        if u:
            return u
        else:
            abort(404)
    abort(401)
