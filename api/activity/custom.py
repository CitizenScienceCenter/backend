import connexion
from sqlalchemy.orm import lazyload, joinedload
from db import Project, User, Submission, Task
from decorators import access_checks
from flask import request, abort
from pony.flask import db_session
from middleware.response_handler import ResponseHandler


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
        return ResponseHandler(200, body=[s.to_dict() for s in a.tasks.limit(limit, offset=offset)]).send()
    elif a and a.tasks.count() == 0:
        return ResponseHandler(200, 'Activity has no tasks', body=[], ok=False).send()
    else:
        abort(404)

@db_session
def get_random_activity_task(id=None, orderBy=None, notDone=False):
    return '', 200
