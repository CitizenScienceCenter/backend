import connexion
from connexion import NoContent
from db import orm_handler, Submission, utils
from decorators import access_checks
from flask import request
import logging
import json
from api import model

db_session = orm_handler.db_session()

Model = Submission

def get_submissions(limit=100, search_term=None):
    ms, code =  model.get_all(Model, limit, search_term)
    if len(ms) > 0 and isinstance(ms[0], Submission):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code

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
