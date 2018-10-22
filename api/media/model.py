import connexion
from connexion import NoContent
from db import orm_handler, utils, Media
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

def get_all(limit=20, search_term=None):
    return model.get_all(Media, limit, search_term)

def get_one(id=None):
    return model.get_one(Media, id)

@access_checks.ensure_key
def post(media):
    return model.post(Model, media)

@access_checks.ensure_key
def put(id, media):
    return model.put(Media, id, media)

@access_checks.ensure_key
def delete(id):
    return model.delete(Media, id)