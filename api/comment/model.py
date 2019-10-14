import connexion
from db.models import Comment
from db import utils
from flask import request, abort
from pony.orm import *
import logging
from api import model

Model = Comment


def get_comments(limit, offset, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()


def get_comment(cid=None):
    return model.get_one(Model, cid).send()


def create_comment(body):
    res, c = model.post(Model, body)
    return res.send()


def update_comment(cid, body):
    res, c = model.put(Model, cid, body)
    return res.send()


def delete_comment(cid):
    return model.delete(Model, cid).send()
