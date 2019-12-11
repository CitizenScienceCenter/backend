from connexion import NoContent
from db import Comment, utils, User, Project, Member, Role
from decorators import access_checks
from flask import request
import logging
from api import model

from pony.flask import db_session

Model = Project


def get_projects(limit=100, offset=0, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()

def get_project(pid=None):
    return model.get_one(Model, pid).send()


@db_session
def create_project(body):
    project = body
    user = utils.get_user(request, db_session)
    project["owner"] = user.id
    role = Role.get(name='owner')
    res, p = model.post(Model, project)
    m = Member(user_id=user, project_id=p, role=role)
    p.members.add(m)
    return res.send()


def update_project(pid, body):
    res, _ = model.put(Model, pid, body)
    return res.send()


@db_session
@access_checks.ensure_owner(Model)
def delete_project(pid):
    # TODO are projects deleted also or anonymised? Transferred to c3s admin?
    return model.delete(Model, pid).send()
