import connexion
from connexion import NoContent
import orm
from decorators import access_checks
from flask import g

def get_projects(limit, search_term=None):
    q = g.db_session.query(orm.Project)
    if search_term:
        q = q.filter(orm.Project.name == search_term)
    return [p.dump() for p in q][:limit]


def get(project_id=None):
    project = g.db_session.query(orm.Project).filter(orm.Project.proj_id == project_id).one_or_none()
    return project.dump() if project is not None else ('Not found', 404)

@access_checks.ensure_key
def create(project):
    logging.info('Creating project ')
    project['proj_id'] = uuid.uuid4()
    project['created_at'] = datetime.datetime.utcnow()
    print(project)
    g.db_session.add(orm.Project(**project))
    g.db_session.commit()
    return NoContent, 201

@access_checks.ensure_key
def put(project_id, project):
    p = g.db_session.query(orm.Projec).filter(orm.Project.id == project_id).one_or_none()
    project['id'] = project_id
    if p is not None:
        logging.info('Updating project %s..', project_id)
        project['updated_at'] = datetime.datetime.utcnow()
        p.update(**project)
    else:
        logging.info('Creating project %s..', project_id)
        project['created_at'] = datetime.datetime.utcnow()
        g.db_session.add(orm.Project(**project))
    g.db_session.commit()
    return NoContent, (200 if p is not None else 201)

@access_checks.ensure_key
def delete(project_id):
    project = g.db_session.query(orm.Project).filter(orm.Project.id == project_id).one_or_none()
    if project is not None:
        logging.info('Deleting project %s..', project_id)
        g.db_session.query(orm.Project).filter(orm.Project.id == project_id).delete()
        g.db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404