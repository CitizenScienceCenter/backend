from db import Submission
from decorators import access_checks, user_checks
from flask import request
from api import model

from pony.flask import db_session

Model = Submission

def get_submissions(limit, offset, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()

def get_submission_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code

def get_submission(id=None):
    return model.get_one(Model, id).send()

@user_checks.multiple_submissions
def create_submission(body):
    res, s = model.post(Model, body)
    return res.send()


def update_submission(id, body):
    res, s = model.put(Model, id, body)
    return res.send()

@access_checks.ensure_owner(Model)
def delete_submission(id):
    return model.delete(Model, id).send()
