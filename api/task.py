import connexion
from connexion import NoContent
from db import orm_handler, Task, Submission, Media, utils
from decorators import access_checks
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload
from flask import request
import sqlalchemy
import logging

db_session = orm_handler.db_session

def get_tasks(limit=20, search_term=None):
    q = db_session.query(Task)
    if search_term:
        q = q.filter(Task.title.match(search_term, postgresql_regconfig='english') | Task.content.match(search_term, postgresql_regconfig='english'))
    return [t.dump() for t in q][:limit]


def get_task(id, detail):
    task = db_session.query(Task).filter(Task.id == id).one_or_none()
    return task.dump() if task is not None else ('Not found', 404)

def get_random(id, search):
    user = utils.get_user(request, db_session)
    task = db_session.query(Task, Media).outerjoin(Submission, Task.id == Submission.task_id).join(Media, Media.source_id == Task.id).filter((Task.info['SchoolState'].astext == search) | (Task.info['SchoolState'].astext == '')).filter((Submission.id == None) | (Submission.user_id != user.id)).order_by(func.random()).first()
    if task is None:
        return NoContent, 404
    else:
        ret = {
            'task': task[0].dump(),
            'media': task[1].dump()
        }
        return ret, 200

@access_checks.ensure_key
def create_tasks(tasks):
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
def project_tasks(id, limit=20):
    task = db_session.query(Task).filter(Task.project_id == id)
    return [p.dump() for p in task][:limit]

@access_checks.ensure_key
def put_task(task_id, task):
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
def delete_tasks(tasks):
    print('deleting {} tasks'.format(len(tasks)))
    print(tasks)
    db_session.query(Task).filter(Task.id.in_(tasks)).delete(synchronize_session='fetch')
    db_session.commit()
    return NoContent, 200

@access_checks.ensure_key
def delete_task(task_id):
    task = db_session.query(Task).filter(Task.id == task_id).one_or_none()
    if task is not None:
        logging.info('Deleting task %s..', project_id)
        db_session.query(Task).filter(Task.id == task_id).delete()
        db_session.commit()
        return {msg: 'Deleted'}, 200
    else:
        return NoContent, 404