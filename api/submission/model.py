import connexion
from connexion import NoContent
from db import orm_handler, Submission, utils
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

def get_submissions(limit=20, search_term=None):
    return model.get_all(Submission, limit, search_term)

def get_submission(id=None):
    return model.get_one(Submission, id)

@access_checks.ensure_key
def create_submission(submission):
    return model.post(Submission, submission)

@access_checks.ensure_key
def update_submission(id, submission):
    return model.put(Submission, id, submission)

@access_checks.ensure_key
def delete_submission(id):
    return model.delete(Submission, id)
