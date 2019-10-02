import logging

import sqlalchemy
from api import model
from connexion import NoContent
from db import Media, Submission, Task
from decorators import access_checks
from flask import request
from pony.flask import db_session
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func

Model = Task


def get_tasks(limit, offset, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()


def get_task_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code


def get_task(id=None):
    return model.get_one(Model, id).send()


def create_task(body):
    res, task = model.post(Model, body)
    return res.send()


def create_tasks(body):
    tasks = body
    res = []
    for task in tasks:
        res, t = model.post(Model, task)
        res.append(t.to_dict())
    return res.send()


def update_task(id, body):
    res, t = model.put(Model, id, body)
    return res.send()


@access_checks.ensure_owner(Model)
def delete_task(id):
    return model.delete(Model, id).send()


# TODO check type expected
def delete_tasks(body):
    for task in body:
        model.delete(Model, task)
    return NoContent, 200
