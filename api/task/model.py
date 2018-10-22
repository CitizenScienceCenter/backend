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

def get_all(limit=20, search_term=None):
    return model.get_all(Task, limit, search_term)

def get_one(id=None):
    return model.get_one(Task, id)

@access_checks.ensure_key
def post(tasks):
    for task in tasks:
        model.post(Task, task)
    return NoContent, 201

@access_checks.ensure_key
def put(id, task):
    return model.put(Task, id, task)

@access_checks.ensure_key
def delete(id):
    return model.delete(Task, id)
