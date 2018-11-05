import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session


def get_comments(limit=20, search_term=None):
    return model.get_all(Comment, limit, search_term)


def get_comment(id=None):
    return model.get_one(Comment, id)


@access_checks.ensure_key
def create_comment(comment):
    logging.info("Creating Comment ")
    return model.post(Comment, comment)


@access_checks.ensure_key
def update_comment(id, comment):
    return model.put(Comment, id, comment)


@access_checks.ensure_key
def delete_comment(id):
    return model.delete(Comment, id)
