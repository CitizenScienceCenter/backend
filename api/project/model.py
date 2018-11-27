import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils, Activity, User, Project
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

Model = Project

def get_projects(limit=20, search_term=None):
    ms, code =  model.get_all(Model, limit, search_term)
    return [dict(m) for m in ms][:limit], code

def get_project_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code

def get_project(id=None):
    m, code = model.get_one(Model, id)
    return m.dump(), code


@access_checks.ensure_key
def create_project(project):
    user = utils.get_user(request, db_session)
    project["owned_by"] = user.id
    p = Model(**project)
    user.member_of.append(p)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(p)
    return p.dump(), 201


@access_checks.ensure_key
def update_project(id, project):
    m, code = model.put(Model, id, project)
    return m.dump(), code


@access_checks.ensure_owner(Model)
def delete_project(id):
    user = utils.get_user(request, db_session)
    project = db_session.query(Model).filter(Model.id==id).one_or_none()
    if project is None:
        return "Project was not found", 404
    users = db_session.query(User).filter(User.member_of.any(Model.id==project.id)).all()
    for u in users:
        u.member_of.remove(project)
    db_session.commit()
    return model.delete(Model, id)
