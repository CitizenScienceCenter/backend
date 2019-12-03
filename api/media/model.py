import connexion
from connexion import NoContent
from db import utils, Media
from decorators import access_checks
from api import model
from pony.flask import db_session

Model = Media


def get_media(limit=100, search_term=None):
    ms, code = model.get_all(Model, limit, search_term)
    if len(ms) > 0 and isinstance(ms[0], Media):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code


def get_medium(mid=None):
    return model.get_one(Model, mid).send()


def create_medium(body):
    res, _ = model.post(Model, body)
    return res.send()

def update_medium(mid, body):
    res, _ = model.put(Model, mid, body)
    return res.send()


def delete_medium(mid):
    res, _ = model.delete(Model, mid)
    return res.send()
