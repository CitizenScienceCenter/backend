import connexion
from connexion import NoContent
from db import utils, Media
from decorators import access_checks
from api import model
from pony.flask import db_session

Model = Media

def get_media(limit=100, search_term=None):
    ms, code =  model.get_all(Model, limit, search_term)
    if len(ms) > 0 and isinstance(ms[0], Media):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code


def get_medium(id=None):
    return model.get_file(Model, id)


def create_medium(body):
    m, code = model.post(Model, body)
    return m.dump(), code

def update_medium(id, body):
    m, code = model.put(Model, id, body)
    return m.dump(), code


def delete_medium(id):
    return model.delete(Model, id)
