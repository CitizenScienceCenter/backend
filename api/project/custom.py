import logging
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app, abort
from db import User, utils, Submission, Project, Task, DB
import smtplib
from email import message
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from decorators import access_checks
from middleware.response_handler import ResponseHandler

ts = URLSafeTimedSerializer("SUPES_SECRET87").signer("SUPES_SECRET87")
from pony.flask import db_session
from pony.orm import commit

RANDOM_USER_TASK = "select * from tasks TABLESAMPLE SYSTEM_ROWS(10000) WHERE tasks.id NOT IN (SELECT submissions.task_id from submissions where submissions.user_id = '{0}') AND tasks.part_of='{1}' LIMIT 1;"

RANDOM_TASK = "select * from tasks TABLESAMPLE SYSTEM_ROWS(10000) WHERE tasks.part_of='{}' LIMIT 1;"


@db_session
@access_checks.ensure_owner(Project)
def publish(pid=None):
    p = Project[pid]
    if p is not None and p.active is False:
        p.info["applied"] = True
        commit()
        return ResponseHandler(200, "Application to publish submitted").send()
    else:
        return ResponseHandler(500, "Project is already published").send()


@db_session
@access_checks.ensure_owner(Project)
def unpublish(pid=None):
    p = Project[pid]
    if p is not None and p.active is True:
        p.active = False
        commit()
        return ResponseHandler(200, "Project unpublished").send()
    else:
        return ResponseHandler(500, "Project is already inactive").send()


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
        data["complete"] = complete
    else:
        abort(404)
    return ResponseHandler(200, "", body=data).send()


@db_session
def get_members(pid):
    p = Project.get(id=pid)
    if p:
        m = [m.to_dict() for m in p.members]
        return ResponseHandler(200, "Project members", body=m).send()
    else:
        abort(404)


@db_session
def get_project_media(pid=None, limit=20, offset=0):
    p = Project.get(id="{}".format(pid))
    if p:
        return [m.to_dict() for m in p.media.limit(limit, offset=offset)]
    else:
        abort(404)


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
def get_project_task(pid=None, index=-1, random=False):
    p = Project.get(id=pid)
    body = None
    print(index, random)
    if p:
        if index >= 0:
            tasks = p.tasks.limit(1, offset=index)
            body = [t.to_dict() for t in tasks]
        else:
            u = utils.get_user(request, db_session)
            task = Task.select_by_sql(RANDOM_USER_TASK.format(u.id, pid))
            if len(task) != 0:
                body = [t.to_dict() for t in task]
            else:
                abort(404, "No Tasks Found")
        return ResponseHandler(200, "Task", body=body).send()
    else:
        abort(404, "Project Not Found")


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
