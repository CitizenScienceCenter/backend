import connexion
from connexion import NoContent
from db import Task, Submission, Media, Project, utils
from api import model
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload
from flask import request
import sqlalchemy
import logging
from sqlalchemy.dialects import postgresql
from pony.flask import db_session

@db_session
def project_tasks(id, limit=20, offset=0):
    tasks = Project[id]
    tasks = Project.get(id=id).tasks
    return [t.to_dict() for t in tasks]

@db_session
def delete_tasks(tasks):
    for t in tasks:
        model.delete(Task, t['id'])
    return NoContent, 200

@db_session
def get_random(pid, search):
    # TODO implement using pg extension
    if task is None:
        return NoContent, 404
    else:
        ret = {"task": task[0].dump(), "media": task[1].dump()}
        return ret, 200
