import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session
from db import orm_handler, OToken
from decorators import access_checks

db_session = orm_handler.init_db()

def generate(request_token):
    # TODO handle if a token already exists and return if it does
    o = OToken()
    o.user_id = request_token.user_id
    o.token_id = uuid.uuid4()
    o.project_id = request_token.project_id
