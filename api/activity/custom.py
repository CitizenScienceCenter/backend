import connexion
from sqlalchemy.orm import lazyload, joinedload
from db import Project, User, Submission, Task
from decorators import access_checks
from flask import request
from pony.flask import db_session


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
