import connexion
from connexion import NoContent
from db import Task, Submission, Media, Project, utils
from api import model
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload
from flask import request, abort
from middleware.response_handler import ResponseHandler
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
def get_task_submissions(tid=None, limit=20, offset=0):
    t = Task[tid]
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
def get_task_media(tid=None, limit=20, offset=0):
    t = Task[tid]
    if t and t.media.count() > 0:
        return ResponseHandler(
            200, "", body=[s.to_dict() for s in t.media.limit(limit, offset=offset)]
        ).send()
    elif t and t.media.count() == 0:
        return ResponseHandler(200, "Task has no submissions", body=[], ok=False).send()
    else:
        abort(404)


@db_session
def get_stats(tid=None):
    task = Task[tid]
    if task is not None:
        data = {
            'task': tid,
            'submissions_count': task.submissions.count()
        }
        return ResponseHandler(200, 'Task Stats', body=data).send()
    else:
        abort(404)


@db_session
def get_random(pid, search):
    # TODO implement using pg extension
    return NoContent, 200
