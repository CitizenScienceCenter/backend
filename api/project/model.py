from connexion import NoContent
from db import Comment, utils, Activity, User, Project
from decorators import access_checks
from flask import request
import logging
from api import model

from pony.flask import db_session

Model = Project


def get_projects(limit=100, offset=0, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()


def get_project_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code


def get_project(id=None):
    return model.get_one(Model, id).send()


@db_session
def create_project(body):
    project = body
    user = utils.get_user(request, db_session)
    project["owned_by"] = user.id
    res, p = model.post(Model, project)
    return res.send()


def update_project(id, body):
    res, p = model.put(Model, id, body)
    return res.send()


@access_checks.ensure_owner(Model)
@db_session
def delete_project(id):
    return model.delete(Model, id).send()
