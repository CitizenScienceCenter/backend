import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils
from decorators import access_checks
from flask import request
import logging
from api import model

# db_session = orm_handler.db_session()

Model = Comment

def get_comments(limit=100, search_term=None):
    ms, code = model.get_all(Model, limit, search_term)
    if len(ms) > 0 and isinstance(ms[0], Comment):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code


def get_comment(id=None):
    m, code = model.get_one(Model, id)
    return m.dump() if m is not None else m, code

def create_comment(comment):
    logging.info("Creating Comment ")
    m, code = model.post(Model, comment)
    return m.dump(), code

def update_comment(id, comment):
    m, code = model.put(Model, id, comment)
    return m.dump(), code

def delete_comment(id):
    return model.delete(Model, id)
