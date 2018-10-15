import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

def get_all(limit=20, search_term=None):
    return model.get_all(Comment, 20, search_term)

def get_one(id=None):
    return model.get_one(Comment, id)

@access_checks.ensure_key
def post(comment):
    logging.info('Creating Comment ')
    return model.post(Comment, comment)

@access_checks.ensure_key
def put(id, comment):
    return model.put(Comment, id, comment)

@access_checks.ensure_key
def delete(id):
    return model.delete(Comment, id)