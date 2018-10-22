import connexion
from connexion import NoContent
from db import orm_handler, Submission, utils
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

def get_all(limit=20, search_term=None):
    return model.get_all(Submission, 20, search_term)

def get_one(id=None):
    return model.get_one(Submission, id)

@access_checks.ensure_key
def post(submission):
    return model.post(Submission, submission)

@access_checks.ensure_key
def put(id, submission):
    return model.put(Submission, id, submission)

@access_checks.ensure_key
def delete(id):
    return model.delete(Submission, id)
