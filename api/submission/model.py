from db import Submission
from decorators import access_checks
from flask import request
from api import model

from pony.flask import db_session

Model = Submission

def get_submissions(limit, offset, search_term=None):
    ms, code =  model.get_all(Model, limit, offset, search_term)
    return [m.to_dict() for m in ms][:limit], code

def get_submission_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code

def get_submission(id=None):
    m, code = model.get_one(Model, id)
    return m.dump(), code


def create_submission(body):
    m, code = model.post(Model, body)
    return m.dump(), code


def update_submission(id, body):
    m, code = model.put(Model, id, body)
    return m.dump(), code

@access_checks.ensure_owner(Model)
def delete_submission(id):
    return model.delete(Model, id)
