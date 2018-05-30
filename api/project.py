import connexion
import logging
from connexion import NoContent
from db import orm_handler, Project, User, utils
from decorators import access_checks
from flask import request


db_session = orm_handler.db_session

def get(limit=20, search_term=None):
    q = db_session.query(Project)
    if search_term:
        q = q.filter(Project.name == search_term)
    return [p.dump() for p in q][:limit]


def get_one(id=None):
    project = db_session.query(Project).filter(Project.id == id).one_or_none()
    return project.dump() if project is not None else ('Not found', 404)

@access_checks.ensure_key
def create(project):
    logging.info('Creating project ')
    user = utils.get_user(request, db_session)
    project['owned_by'] = user.id
    p = Project(**project)
    db_session.add(p)
    db_session.commit()
    return p.dump(), 201

@access_checks.ensure_key
def put(project_id, project):
    p = db_session.query(Project).filter(Project.id == project_id).one_or_none()
    project['id'] = project_id
    if p is not None:
        logging.info('Updating project %s..', project_id)
        p.update(**project)
    else:
        logging.info('Creating project %s..', project_id)
        db_session.add(Project(**project))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)

@access_checks.ensure_key
def delete(project_id):
    project = db_session.query(Project).filter(Project.id == project_id).one_or_none()
    if project is not None:
        logging.info('Deleting project %s..', project_id)
        db_session.query(Project).filter(Project.id == project_id).delete()
        db_session.commit()
        return {msg: 'Deleted'}, 200
    else:
        return NoContent, 404