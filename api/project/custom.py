import logging
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app, abort
from db import User, utils, Submission, Project
import smtplib
from email import message
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from decorators import access_checks
from middleware.response_handler import ResponseHandler

ts = URLSafeTimedSerializer("SUPES_SECRET87").signer("SUPES_SECRET87")
from pony.flask import db_session

RANDOM_TASK = "select * from tasks TABLESAMPLE SYSTEM_ROWS(1) LEFT JOIN submissions on tasks.id=submissions.task_id WHERE (submissions.task_id IS NULL OR submissions.user_id != '{0}') AND tasks.activity_id='{1}';"

@db_session
def get_stats(pid=None):
    p = Project[pid]
    task_count = 0
    tasks = []
    complete = 0
    data = {"task_count": task_count, "tasks": tasks, "complete": 0}
    if p is not None:
        task_count = p.tasks.count()
        tasks = p.tasks
        for t in p.tasks:
            if t.submissions.count() > 0:
                complete += 1
        data['complete'] = complete
    else:
        abort(404)
    return ResponseHandler(200, "", body=data).send()


@db_session
def get_project_tasks(pid=None, limit=20, offset=0):
    p = Project[pid]
    if p and p.tasks.count() > 0:
        return ResponseHandler(
            200,
            {"offset": offset, "limit": limit, "total": p.tasks.count()},
            body=[s.to_dict() for s in p.tasks.limit((limit), offset=(offset))],
        ).send()
    elif p and p.tasks.count() == 0:
        return ResponseHandler(200, "Project has no tasks", body=[], ok=False).send()
    else:
        abort(404)


@db_session
def get_random_project_task(aid=None, orderBy=None, notDone=False):
    u = utils.get_user(request, db_session)
    p = Project[pid]
    t = p.tasks.get_by_sql(RANDOM_TASK.format(u.id, a.id))
    return ResponseHandler(200, "Task", body=t.to_dict()).send()


@db_session
@access_checks.ensure_owner(Project)
def get_project_submissions(pid, limit=20, offset=0):
    p = Project.get(id="{}".format(pid))
    if p:
        return [s.to_dict() for s in p.submissions.limit(limit, offset=offset)]
    else:
        abort(404)


@db_session
def get_project_activities(pid, limit=20, offset=0):
    p = Project.get(id="{}".format(pid))
    if p and p.activities.count() > 0:
        return ResponseHandler(
            200,
            "",
            body=[s.to_dict() for s in p.activities.limit(limit, offset=offset)],
        ).send()
    elif p and p.activities.count() == 0:
        return ResponseHandler(
            200, "Project has no activities", body=[], ok=False
        ).send()
    else:
        abort(404)
