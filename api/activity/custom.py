import connexion
from flask import abort, request
from pony.flask import db_session
from sqlalchemy.orm import joinedload, lazyload

from db import Activity, Project, Submission, Task, User, utils
from decorators import access_checks
from middleware.response_handler import ResponseHandler

RANDOM_TASK = "select * from tasks LEFT JOIN submissions on tasks.id=submissions.task_id WHERE (submissions.task_id IS NULL OR submissions.user_id != '{0}') AND tasks.activity_id='{1}' ORDER BY random() LIMIT 1;"


@db_session
def activity_stats(aid=None):
    a = Activity[aid]
    task_count = 0
    tasks = []
    data = {"task_count": task_count, "tasks": tasks, "complete": 0}
    if a is not None:
        task_count = a.tasks.count()
        tasks = a.tasks
    else:
        abort(404)
    return ResponseHandler(200, "", body=data).send()


@db_session
def get_activity_tasks(aid=None, limit=20, offset=0):
    a = Activity[aid]
    if a and a.tasks.count() > 0:
        return ResponseHandler(
            200,
            {"offset": offset, "limit": limit, "total": a.tasks.count()},
            body=[s.to_dict() for s in a.tasks.limit((limit), offset=(offset))],
        ).send()
    elif a and a.tasks.count() == 0:
        return ResponseHandler(200, "Activity has no tasks", body=[], ok=False).send()
    else:
        abort(404)


@db_session
def get_random_activity_task(aid=None, orderBy=None, notDone=False):
    u = utils.get_user(request, db_session)
    a = Activity[aid]
    t = a.tasks.get_by_sql(RANDOM_TASK.format(u.id, a.id))
    return ResponseHandler(200, "Task", body=t.to_dict()).send()
