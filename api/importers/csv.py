from db import Task, Project, DB
from api import model
import uuid
from middleware.response_handler import ResponseHandler
from flask import session, request, current_app, abort
from datetime import datetime
from pony.orm import core, commit, select
from pony.flask import db_session

@db_session
def import_csv(pid, body):
    p = Project.get(id=pid)
    tasks = []
    if p:
        for row in body:
            try:
                if len(row.keys()) > 0 and row['part_of'] and row['title']:
                    row['part_of'] = p.id
                    res, t = model.post(Task, row)
                    tasks.append(t.to_dict())
            except Exception as e:
                abort(500, e)
        return ResponseHandler(201, "Tasks imported successfully", body=tasks).send()
    else:
        return ResponseHandler(404, "No Project Found", body={}).send()

@db_session
def import_remote_csv(pid, content):
    pass

