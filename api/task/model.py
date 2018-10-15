import connexion
from connexion import NoContent
from db import orm_handler, Task, Submission, Media, utils
from decorators import access_checks
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload
from flask import request
import sqlalchemy
import logging
from sqlalchemy.dialects import postgresql

db_session = orm_handler.db_session

def get_all(offset=0, search_term=None, limit=20):
    q = db_session.query(Task)
    q = q.offset(offset)
    if search_term:
        q = q.filter(Task.title.match(search_term, postgresql_regconfig='english') | Task.content.match(search_term, postgresql_regconfig='english'))
    q = q.limit(limit)
    return [t.dump() for t in q]


def get_one(id):
    task = db_session.query(Task).filter(Task.id == id).one_or_none()
    return task.dump() if task is not None else ('Not found', 404)

@access_checks.ensure_key
def post(tasks):
    logging.info('Creating tasks for project ')
    saved_tasks = []
    for t in tasks:
        task = Task(**t)
        task.sequence = int(task.sequence)
        print(task)
        db_session.add(task)
        saved_tasks.append(task)
    db_session.commit()
    print(saved_tasks[0].id)
    return [t.dump() for t in saved_tasks][:len(saved_tasks)], 201

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
def delete(task_id):
    task = db_session.query(Task).filter(Task.id == task_id).one_or_none()
    if task is not None:
        logging.info('Deleting task %s..', project_id)
        db_session.query(Task).filter(Task.id == task_id).delete()
        db_session.commit()
        return {msg: 'Deleted'}, 200
    else:
        return NoContent, 404