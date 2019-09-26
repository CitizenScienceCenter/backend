import connexion
from flask import abort, request
from pony.flask import db_session
from sqlalchemy.orm import joinedload, lazyload

from db import Activity, Project, Submission, Task, User, utils
from decorators import access_checks
from middleware.response_handler import ResponseHandler

RANDOM_TASK = "select * from tasks LEFT JOIN submissions on tasks.id=submissions.task_id WHERE (submissions.task_id IS NULL OR submissions.user_id != '{0}') AND tasks.activity_id='{1}' ORDER BY random() LIMIT 1;"


@db_session
def activity_stats(id=None):
    tasks = db_session.query(Task).filter(Task.project_id == id).all()
    no_tasks = len(tasks)
    subs = 0
    cons = []
    for t in tasks:
        submissions = (
            db_session.query(Submission).filter(Submission.task_id == t.id).all()
        )
        subs += len(submissions)
        for s in submissions:
            uid = s.user_id
            if uid not in cons:
                cons.append(uid)
    return (
        {
            "activity_id": id,
            "task_count": no_tasks,
            "submission_count": subs,
            "contributor_count": len(cons),
        },
        200,
    )


@db_session
def get_activity_tasks(id=None, limit=20, offset=0):
    a = Activity.get(id=id)
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
def get_random_activity_task(id=None, orderBy=None, notDone=False):
    u = utils.get_user(request, db_session)
    a = Activity.get(id=id)
    t = a.tasks.get_by_sql(RANDOM_TASK.format(u.id, a.id))
    return ResponseHandler(200, "Task", body=t.to_dict()).send()
