import connexion
import logging
from connexion import NoContent
from sqlalchemy.orm import lazyload, joinedload
from db import orm_handler, Project, User, Submission, Task, utils
from decorators import access_checks
from flask import request

db_session = orm_handler.db_session

def get_stats(id=None):
    tasks = db_session.query(Task).filter(Task.project_id == id).all()
    no_tasks = len(tasks)
    subs = 0
    cons = []
    for t in tasks:
        submissions = db_session.query(Submission).filter(Submission.task_id == t.id).all()
        subs += len(submissions)
        for s in submissions:
            uid = s.user_id
            if uid not in cons:
                cons.append(uid)
    return {'project_id': id, 'task_count': no_tasks, 'submission_count': subs, 'contributor_count': len(cons)}, 200