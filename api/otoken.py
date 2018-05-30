import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request
from db import orm_handler, OToken
from decorators import access_checks

db_session = orm_handler.db_session

def generate(token):
    o_token = OToken(**token)
    p = db_session.query(OToken).filter(OToken.user_id == o_token.user_id and OToken.project_id == o_token.project_id).one_or_none()
    if p is None:
        db_session.add(o_token)
        db_session.commit()
        return o_token.dump(), 201
    else:
        return p.dump(), 200
