import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request
from db import orm_handler, OToken
from decorators import access_checks

db_session = orm_handler.init_db()

def generate(token):
    # TODO handle if a token already exists and return if it does
    o_token = OToken(**token)
    db_session.add(o_token)
    db_session.commit()
    return o_token.dump(), 201
