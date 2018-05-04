import connexion
from connexion import NoContent
from orm import orm_handler, User
from decorators import access_checks

db_session = orm_handler.init_db()

def get_projects(limit, search_term=None):
    q = db_session.query(Project)
    if search_term:
        q = q.filter(Project.name == search_term)
    return [p.dump() for p in q][:limit]


def get(project_id=None):
    project = db_session.query(Project).filter(Project.proj_id == project_id).one_or_none()
    return project.dump() if project is not None else ('Not found', 404)

@access_checks.ensure_key
def create(project):
    logging.info('Creating project ')
    project['proj_id'] = uuid.uuid4()
    project['created_at'] = datetime.datetime.utcnow()
    print(project)
    db_session.add(Project(**project))
    db_session.commit()
    return NoContent, 201

@access_checks.ensure_key
def put(project_id, project):
    p = db_session.query(Projec).filter(Project.id == project_id).one_or_none()
    project['id'] = project_id
    if p is not None:
        logging.info('Updating project %s..', project_id)
        project['updated_at'] = datetime.datetime.utcnow()
        p.update(**project)
    else:
        logging.info('Creating project %s..', project_id)
        project['created_at'] = datetime.datetime.utcnow()
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
        return NoContent, 204
    else:
        return NoContent, 404