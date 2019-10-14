from db import Submission, User, Task, Activity
from decorators import access_checks, user_checks
from flask import request, abort
from api import model

from pony.flask import db_session

from middleware.response_handler import ResponseHandler


@db_session
@access_checks.ensure_owner
def get_user_submissions(uid):
    user = User.get(id=uid)
    subs = user.submissions
    return ResponseHandler(200, "Submissions for user", body=subs)


@db_session
# TODO access check for project members and user
# TODO add to openapi spec as /task/:id/submissions/:uid
def get_user_task_submissions(uid, tid):
    user = User.get(id=uid)
    task = Task.get(id=tid)
    if task and user:
        subs = Task.get(id=tid).submissions.where(user_id=uid)
        return ResponseHandler(200, "Submissions for user", body=subs)
    else:
        abort(404)


# TODO add to openapi spec as /activity/:id/submissions/:uid
@db_session
def get_activity_submissions(aid, uid=None):
    user = None
    if uid is not None:
        user = User.get(id=uid)
    activity = Activity.get(id=aid)
    if (user and uid) and activity:
        subs = {}
        for task in Activity.tasks:
            if uid:
                subs[task.id] = task.submissions.where(user_id=uid)
            else:
                subs[task.id] = task.submissions.where()
        return ResponseHandler(200, "Activity Submissions for User", body=subs)
    else:
        abort(404)
