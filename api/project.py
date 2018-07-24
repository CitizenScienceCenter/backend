import connexion
import logging
from connexion import NoContent
from sqlalchemy.orm import lazyload, joinedload
from db import orm_handler, Project, User, Submission, Task, utils
from decorators import access_checks
from flask import request


db_session = orm_handler.db_session

def get_projects(limit=20, search_term=None):
    q = db_session.query(Project)
    if search_term:
        q = q.filter(Project.name.match(search_term, postgresql_regconfig='english') | Project.description.match(search_term, postgresql_regconfig='english'))
    return [p.dump() for p in q][:limit]


def get_project(id=None):
    project = db_session.query(Project).filter(Project.id == id).one_or_none()
    return project.dump() if project is not None else ('Not found', 404)

@access_checks.ensure_key
def create_project(project):
    logging.info('Creating project ')
    user = utils.get_user(request, db_session)
    project['owned_by'] = user.id
    p = Project(**project)
    db_session.add(p)
    db_session.commit()
    print(p.id)
    return p.dump(), 201

@access_checks.ensure_key
def put_project(project_id, project):
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
def delete_project(id):
    project = db_session.query(Project).filter(Project.id == id).one_or_none()
    if project is not None:
        logging.info('Deleting project %s..', id)
        db_session.query(Task).filter(Task.project_id == id).delete()
        db_session.query(Project).filter(Project.id == id).delete()
        # TODO combine and handle deletion of submissions (export first?)
        db_session.commit()
        return {'msg': 'Deleted'}, 200
    else:
        return NoContent, 404   