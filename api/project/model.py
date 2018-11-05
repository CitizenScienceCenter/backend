import connexion
import logging
from connexion import NoContent
from sqlalchemy.orm import lazyload, joinedload
from db import orm_handler, Project, User, Submission, Task, utils
from decorators import access_checks
from flask import request
from api import model


db_session = orm_handler.db_session

def get_projects(limit=20, search_term=None):
    return model.get_all(Project, limit, search_term)

def get_project(id=None):
    return model.get_one(Project, id)

@access_checks.ensure_key
def create_project(project):
    user = utils.get_user(request, db_session)
    project['owned_by'] = user.id
    return model.post(Project, project)

@access_checks.ensure_key
def update_project(id, project):
    return model.put(Project, id, project)

@access_checks.ensure_owner(Project)
def delete_project(id):
    # TODO delete tasks first
    return model.delete(Project, id)