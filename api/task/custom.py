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
def delete_tasks(tasks):
    for t in tasks:
        model.delete(Task, t["id"])
    return NoContent, 200


@db_session
def get_task_submissions(id=None, limit=20, offset=0):
    t = Task.get(id=id)
    if t and t.submissions.count() > 0:
        return ResponseHandler(
            200,
            "",
            body=[s.to_dict() for s in t.submissions.limit(limit, offset=offset)],
        ).send()
    elif t and t.submissions.count() == 0:
        return ResponseHandler(200, "Task has no submissions", body=[], ok=False).send()
    else:
        abort(404)


@db_session
def get_task_media(id=None, limit=20, offset=0):
    t = Task.get(id=id)
    if t and t.media.count() > 0:
        return ResponseHandler(
            200, "", body=[s.to_dict() for s in t.media.limit(limit, offset=offset)]
        ).send()
    elif t and t.media.count() == 0:
        return ResponseHandler(200, "Task has no submissions", body=[], ok=False).send()
    else:
        abort(404)


@db_session
def get_stats(id=None):
    pass


@db_session
def get_random(pid, search):
    # TODO implement using pg extension
    return NoContent, 200
