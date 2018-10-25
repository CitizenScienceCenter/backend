import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app
from db import orm_handler, User, utils, Submission
from decorators import access_checks
import json, smtplib
import email as emaillib
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from api import model

db_session = orm_handler.db_session


def get_users(limit=20, search_term=None):
    return model.get_all(User, limit, search_term)

def get_user(id=None):
    return model.get_one(User, id)

def create_user(user):
    user['api_key'] = uuid.uuid4()
    user['pwd'] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(user['pwd'])
    print(user)
    if ('username' in user and len(user['username']) == 0) or not 'username' in user:
        user['username'] = user['email']
    return model.post(User, user)

@access_checks.ensure_key
def update_user(id, user):
    # TODO ensure only user can edit their own profile
    return model.put(User, id, user)

@access_checks.ensure_key
def delete_user(id):
    # TODO ensure only user can delete their own profile
    return model.delete(User, id)
