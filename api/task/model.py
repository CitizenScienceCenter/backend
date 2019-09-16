from connexion import NoContent
from db import Task, Submission, Media
from decorators import access_checks
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload
from flask import request
import sqlalchemy
import logging
from sqlalchemy.dialects import postgresql
from api import model

from pony.flask import db_session

Model = Task

def get_tasks(limit, offset, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()

def get_task_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code


def get_task(id=None):
    return model.get_one(Model, id).send()

def create_task(body):
    res, task = model.post(Model, task)
    return res.send()


def create_tasks(body):
    tasks = body
    res = []
    for task in tasks:
        res, t = model.post(Model, task)
        res.append(t.to_dict())
    return res, 201

def update_task(id, body):
    res, t = model.put(Model, id, body)
    return res.send()


def delete_task(id):
    return model.delete(Model, id).send()

# TODO check type expected
def delete_tasks(tasks):
    for task in tasks:
        model.delete(Model, task)
    return NoContent, 200
