import connexion
from sqlalchemy.orm import lazyload
from decorators import access_checks
from flask import request
from api import model
from db import Member

from pony.flask import db_session

Model = Member

def get_members(limit=20, offset=0, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()

def get_member(mid=None):
    return model.get_one(Model, mid).send()

def create_member(body):
    res, a = model.post(Model, body)
    return res.send()

@db_session
@access_checks.ensure_owner(Model)
def delete_member(mid):
    # TODO delete tasks first? Or set info to deleted?
    return model.delete(Model, mid).send()


def update_member(mid, body):
    return model.put(Model, mid, body)[0].send()
