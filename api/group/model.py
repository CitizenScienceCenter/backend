import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils, Group
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

def get_all(limit=20, search_term=None):
    return model.get_all(Group, 20, search_term)

def get_one(id=None):
    return model.get_one(Group, id)

@access_checks.ensure_key
def post(group):
    logging.info('Creating Comment ')
    return model.post(Group, group)

@access_checks.ensure_key
def put(id, group):
    return model.put(Group, id, group)

@access_checks.ensure_key
def delete(id):
    return model.delete(Group, id)