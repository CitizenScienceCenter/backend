import connexion
from db.models import Comment
from db import utils
from flask import request, abort
from pony.orm import *
import logging
from api import model

# db_session = orm_handler.db_session

Model = Comment

def get_comments(limit=100, search_term=None):
    # TODO handle jtos here
    c = Comments.search().limit(limit)
    return [c.to_dict() for c in comments][:limit], 200


def get_comment(cid=None):
    try:
        c = Comment[id]
    except core.ObjectNotFound:
        abort(401)
    return c.to_dict(), 200

def create_comment(body):
    c = Comment(**body)
    commit()
    return c.to_dict(), 201

def update_comment(id, body):
    m, code = model.put(Model, id, body)
    return m.dump(), code

def delete_comment(id):
    return model.delete(Model, id)
