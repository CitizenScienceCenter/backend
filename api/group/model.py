import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils, Group
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

def get_groups(limit=20, search_term=None):
    return model.get_all(Group, limit, search_term)

def get_group(id=None):
    return model.get_one(Group, id)

@access_checks.ensure_key
def create_group(group):
    user = utils.get_user(request, db_session)
    group['created_by'] = user.id
    return model.post(Group, group)

@access_checks.ensure_key
def update_group(id, group):
    return model.put(Group, id, group)

@access_checks.ensure_key
def delete_group(id):
    return model.delete(Group, id)