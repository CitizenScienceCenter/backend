import connexion
from sqlalchemy.orm import lazyload
from decorators import access_checks
from flask import request
from api import model
from db import *

# from flask_sqlalchemy_session import current_session as db_session

Model = Activity

@db_session
def get_activities(limit=100, search_term=None):
    a = Activity.select()
    print(a)
    for b in a:
        print(a)
    return None, 200

@db_session
def get_activity_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code

@db_session
def get_activity(id=None):
    a = Activity.select(lambda a: a.id == id)
    print(a)
    return a if a is not None else m, code

@db_session
def create_activity(body):
    a = Activity(**body)
    print(a)
    m, code = model.post(Model, body)
    return m.dump(), code


@access_checks.ensure_owner(Model)
def delete_activity(id):
    # TODO delete tasks first
    return model.delete(Model, id)

def update_activity(id, body):
    m, code = model.put(Model, id, body)
    return m.dump(), code
