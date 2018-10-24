import connexion
from connexion import NoContent
from db import orm_handler, utils, Media
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session

def get_media(limit=20, search_term=None):
    return model.get_all(Media, limit, search_term)

def get_medium(id=None):
    return model.get_file(Media, id)

@access_checks.ensure_key
def create_medium(media):
    return model.post(Model, media)

@access_checks.ensure_key
def update_medium(id, media):
    return model.put(Media, id, media)

@access_checks.ensure_key
def delete_medium(id):
    return model.delete(Media, id)