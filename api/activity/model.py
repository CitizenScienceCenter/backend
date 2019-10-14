import connexion
from sqlalchemy.orm import lazyload
from decorators import access_checks
from flask import request
from api import model
from db import Activity

from pony.flask import db_session

Model = Activity


def get_activities(limit=20, offset=0, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()


def get_activity_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code


def get_activity(aid=None):
    return model.get_one(Model, aid).send()


def create_activity(body):
    res, a = model.post(Model, body)
    return res.send()


@db_session
@access_checks.ensure_owner(Model)
def delete_activity(aid):
    # TODO delete tasks first? Or set info to deleted?
    return model.delete(Model, aid).send()


def update_activity(aid, body):
    return model.put(Model, aid, body).send()
