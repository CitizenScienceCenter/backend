import connexion
from connexion import NoContent
from db import orm_handler, Task
from decorators import access_checks
import logging

db_session = orm_handler.db_session

def get(limit=20, search_term=None):
    q = db_session.query(Task)
    if search_term:
        q = q.filter(Task.name == search_term)
    return [p.dump() for p in q][:limit]


def get_one(id=None):
    task = db_session.query(Task).filter(Task.id == id).one_or_none()
    return task.dump() if project is not None else ('Not found', 404)

@access_checks.ensure_key
def create(tasks):
    logging.info('Creating tasks for project ')
    for t in tasks:
        task = Task(**t)
        print(task)
        db_session.add(task)
        db_session.commit()
    return NoContent, 201

@access_checks.ensure_key
def project_tasks(id, limit=20):
    task = db_session.query(Task).filter(Task.project_id == id)
    return [p.dump() for p in task][:limit]

@access_checks.ensure_key
def put(task_id, task):
    t = db_session.query(Task).filter(Task.id == task_id).one_or_none()
    if t is not None:
        logging.info('Updating task %s..', task_id)
        p.update(**project)
    else:
        logging.info('Creating task %s..', task_id)
        db_session.add(Task(**task))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)

@access_checks.ensure_key
def delete(tasks):
    for task in tasks:
        task = db_session.query(Task).filter(Task.id == task_id).one_or_none()
        if task is not None:
            logging.info('Deleting task %s..', project_id)
            db_session.query(Task).filter(Task.id == task_id).delete()
            db_session.commit()
            return {msg: 'Deleted'}, 200
        else:
            return NoContent, 404

@access_checks.ensure_key
def delete_one(task_id):
    task = db_session.query(Task).filter(Task.id == task_id).one_or_none()
    if task is not None:
        logging.info('Deleting task %s..', project_id)
        db_session.query(Task).filter(Task.id == task_id).delete()
        db_session.commit()
        return {msg: 'Deleted'}, 200
    else:
        return NoContent, 404