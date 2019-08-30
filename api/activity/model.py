import connexion
import logging
from connexion import NoContent
from sqlalchemy.orm import lazyload, joinedload
from db import orm_handler, Activity
from decorators import access_checks
from flask import request
from api import model


db_session = orm_handler.db_session()

Model = Activity

def get_activities(limit=100, search_term=None):
    ms, code = model.get_all(Model, limit, search_term)
    print(ms)
    if len(ms) > 0 and isinstance(ms[0], Activity):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code

def get_activity_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code

def get_activity(id=None):
    m, code = model.get_one(Model, id)
    return m.dump() if m is not None else m, code

def create_activity(activity):
    m, code = model.post(Model, activity)
    return m.dump(), code


@access_checks.ensure_owner(Model)
def delete_activity(id):
    # TODO delete tasks first
    return model.delete(Model, id)

def update_activity(id, activity):
    m, code = model.put(Model, id, activity)
    return m.dump(), code
