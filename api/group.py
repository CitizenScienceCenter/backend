import connexion
import logging
from connexion import NoContent
from sqlalchemy.orm import lazyload, joinedload
from db import orm_handler, Project, User, Submission, Task, utils, Group
from decorators import access_checks
from flask import request


db_session = orm_handler.db_session

def get_group(id=None):
    return {}

def get_groups(limit=20, search_term=None):
    return {}

def create(organistaion):
    return {}

def put_group(id, organisation):
    return {}