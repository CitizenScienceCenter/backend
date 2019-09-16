import connexion
from sqlalchemy.orm import lazyload
from decorators import access_checks
from flask import request
from api import model
from db import *

from pony.flask import db_session

Model = Activity


def get_activities(limit, offset, search_term=None):
    ms, code =  model.get_all(Model, limit, offset, search_term)
    return [m.to_dict() for m in ms][:limit], code

def get_activity_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code

def get_activity(id=None):
    a, code = model.get_one(Model, id)
    return a, code

def create_activity(body):
    a, code = model.post(Model, body)
    return a.to_dict(), code

@db_session
@access_checks.ensure_owner(Model)
def delete_activity(id):
    # TODO delete tasks first
    return model.delete(Model, id)

def update_activity(id, body):
    return model.put(Model, id, body)
    return m.dump(), code
