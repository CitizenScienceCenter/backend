import connexion
from connexion import NoContent

import orm

db_session = orm.init_db('postgresql://pybossa:tester@localhost/cccs')

def get_projects(limit, search_term=None):
    q = db_session.query(orm.Project)
    if search_term:
        q = q.filter(orm.Project.name == search_term)
    return [p.dump() for p in q][:limit]


def get_project(project_id=None):
    project = db_session.query(orm.Project).filter(orm.Project.proj_id == project_id).one_or_none()
    return project.dump() if project is not None else ('Not found', 404)


def post_project(project):
    logging.info('Creating project ')
    project['proj_id'] = uuid.uuid4()
    project['created_at'] = datetime.datetime.utcnow()
    print(project)
    db_session.add(orm.Project(**project))
    db_session.commit()
    return NoContent, 201

def put_project(project_id, project):
    p = db_session.query(orm.Projec).filter(orm.Project.id == project_id).one_or_none()
    project['id'] = project_id
    if p is not None:
        logging.info('Updating project %s..', project_id)
        project['updated_at'] = datetime.datetime.utcnow()
        p.update(**project)
    else:
        logging.info('Creating project %s..', project_id)
        project['created_at'] = datetime.datetime.utcnow()
        db_session.add(orm.Project(**project))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_project(project_id):
    project = db_session.query(orm.Project).filter(orm.Project.id == project_id).one_or_none()
    if project is not None:
        logging.info('Deleting project %s..', project_id)
        db_session.query(orm.Project).filter(orm.Project.id == project_id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404