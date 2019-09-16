import connexion
from db.models import Comment
from db import utils
from flask import request, abort
from pony.orm import *
import logging
from api import model

Model = Comment

def get_comments(limit, offset, search_term=None):
    ms, code =  model.get_all(Model, limit, offset, search_term)
    return [m.to_dict() for m in ms][:limit], code


def get_comment(cid=None):
    return model.get_one(Model, cid)

def create_comment(body):
    return model.Post(Model, body)

def update_comment(id, body):
    m, code = model.put(Model, id, body)
    return m.dump(), code

def delete_comment(id):
    return model.delete(Model, id)
