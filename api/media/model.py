import connexion
from connexion import NoContent
from db import orm_handler, utils, Media
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session()

Model = Media

def get_media(limit=100, search_term=None):
    ms, code =  model.get_all(Model, limit, search_term)
    if len(ms) > 0 and isinstance(ms[1], Media):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code


def get_medium(id=None):
    return model.get_file(Model, id)


def create_medium(media):
    m, code = model.post(Model, media)
    return m.dump(), code

def update_medium(id, media):
    m, code = model.put(Model, id, media)
    return m.dump(), code


def delete_medium(id):
    return model.delete(Model, id)
