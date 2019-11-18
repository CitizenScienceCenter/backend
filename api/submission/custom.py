from db import Submission, User, Task, Project
from decorators import access_checks, user_checks
from flask import request, abort
from api import model

from pony.flask import db_session

from middleware.response_handler import ResponseHandler


@db_session
@access_checks.ensure_owner(Submission)
def get_user_submissions(uid):
    user = User.get(id=uid)
    subs = user.submissions
    return ResponseHandler(200, "Submissions for user", body=subs)


@db_session
def get_user_task_submissions(uid, tid):
    user = User.get(id=uid)
    task = Task.get(id=tid)
    if task and user:
        subs = Task.get(id=tid).submissions.where(user_id=uid)
        return ResponseHandler(200, "Submissions for user", body=subs)
    else:
        abort(404)

@db_session
@access_checks.ensure_owner(Project)
def get_project_submissions(pid):
    p = Project.get(id=pid)
    if p:
        subs = {}
        for task in Project.tasks:
            subs[task.id] = task.submissions
        return ResponseHandler(200, "Project Submissions for User", body=subs)
    else:
        abort(404)

@db_session
def get_project_user_submissions(pid, uid):
    user = User[uid]
    project = Project.get(id=pid)
    if user and project:
        subs = {}
        for task in Project.tasks:
            subs[task.id] = task.submissions.where(user_id=uid)
        return ResponseHandler(200, "Project Submissions for User", body=subs)
    else:
        abort(404)
