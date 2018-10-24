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

db_session = orm_handler.db_session

def get_tasks(limit=20, search_term=None):
    return model.get_all(Task, limit, search_term)

def get_task(id=None):
    return model.get_one(Task, id)

@access_checks.ensure_key
def create_tasks(tasks):
    for task in tasks:
        model.post(Task, task)
    return NoContent, 201

@access_checks.ensure_key
def update_task(id, task):
    return model.put(Task, id, task)

@access_checks.ensure_key
def delete_task(id):
    return model.delete(Task, id)

@access_checks.ensure_key
def delete_tasks(tasks):
    for task in tasks:
        model.delete(Task, task)
    return NoContent, 200
