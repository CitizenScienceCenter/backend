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
from api import model

db_session = orm_handler.db_session()

Model = Task

def get_tasks(limit=100, search_term=None):
    ms, code =  model.get_all(Model, limit, search_term)
    if len(ms) > 0 and isinstance(ms[0], Task):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code

def get_task_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code


def get_task(id=None):
    m, code = model.get_one(Model, id)
    return m.dump(), code


def create_tasks(body):
    for task in body:
        model.post(Model, task)
    return NoContent, 201


def update_task(id, task):
    m, code = model.put(Model, id, task)
    return m.dump(), code


def delete_task(id):
    return model.delete(Model, id)


def delete_tasks(tasks):
    for task in tasks:
        model.delete(Model, task)
    return NoContent, 200
