from db.models import User, Task, Submission
from flask import abort
from pony.flask import db_session
from pony.orm import *
import uuid


@db_session
def get_user(request, db):
    if "X-API-KEY" in request.headers:
        key = request.headers["X-API-KEY"]
        u = User.get(api_key=key)
        if u:
            return u
        else:
            abort(404)
    abort(401)

def calc_completed_tasks(tasks, uid=None):
    questions = [t.content['question'] for t in tasks]
    subs = None
    if uid:
        subs = Task.submissions.where(user_id = uid)
    else:
        subs = Task.submissions
    # TODO check submissions response against task question here, could be a view in PG on task submission? 


