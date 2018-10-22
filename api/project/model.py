import connexion
import logging
from connexion import NoContent
from sqlalchemy.orm import lazyload, joinedload
from db import orm_handler, Project, User, Submission, Task, utils
from decorators import access_checks
from flask import request
from api import model


db_session = orm_handler.db_session

def get_all(limit=20, search_term=None):
    return model.get_all(Project, 20, search_term)

def get_one(id=None):
    return model.get_one(Project, id)

@access_checks.ensure_key
def post(project):
    user = utils.get_user(request, db_session)
    project['owned_by'] = user.id
    return model.post(Project, project)

@access_checks.ensure_key
def put(id, project):
    return model.put(Project, id, project)

@access_checks.ensure_key
def delete(id):
    # TODO delete tasks first
    return model.delete(Project, id)