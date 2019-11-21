from db import Task, Project, DB
from middleware.response_handler import ResponseHandler
from flask import session, request, current_app, abort
from datetime import datetime
from pony.orm import core, commit, select
from pony.flask import db_session

@db_session
def import__csv(pid, content):
    for row in content:
        try:
            t = Task(**row)
            commit()
        except Exception as e:
            abort(500, e)
    return ResponseHandler(201, "Tasks importedsuccessfully", body={}).send()

@db_session
def import_remote_csv(pid, content):
    pass

