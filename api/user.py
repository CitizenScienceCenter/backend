import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request
from db import orm_handler, User
from decorators import access_checks
import json

db_session = orm_handler.db_session

def get_users(limit=20, search_term=None):
    q = db_session.query(User)
    print(search_term)
    if search_term:
        q = q.filter(User.email.match(search_term, postgresql_regconfig='english') | User.api_key.match(search_term, postgresql_regconfig='english') | User.id.match(search_term, postgresql_regconfig='english') | User.username.match(search_term, postgresql_regconfig='english'))
    return [u.dump() for u in q][:limit]

def get_user(id):
    # user = db_session.query(User).filter(User.email.match(id, postgresql_regconfig='english') | User.api_key.match(id, postgresql_regconfig='english') | User.id.match(id, postgresql_regconfig='english') | User.username.match(id, postgresql_regconfig='english')).one_or_none()
    user = db_session.query(User).filter(User.id == id).one_or_none()
    return user.dump() if user is not None else ('Not found', 404)

def auth(user):
    # TODO create oauth token here and add to table. Just send api key for now
    q = db_session.query(User).filter(User.email == user['email']).one_or_none()
    if q:
        if pbkdf2_sha256.verify(user['pwd'], q.pwd):
            session['user'] = q.dump()
            return q.dump(), 200
        else:
            return NoContent, 401
    else:
        return NoContent, 404    

def register_user(user):
    logging.info('Creating user ')
    user['api_key'] = uuid.uuid4()
    user['pwd'] = pbkdf2_sha256.encrypt(user['pwd'], rounds=200000, salt_size=16)
    u = User(**user)
    try:
        db_session.add(u)
        db_session.commit()
        return u.dump(), 201
    except Exception as e:
        print(e)
        logging.error('User already registered or unrecoverable error occurred')
        return NoContent, 400

def validate(key):
    q = db_session.query(User).filter(User.api_key == key).one_or_none()
    if q:
        return q.dump(), 201
    else:
        return NoContent, 401

def login(user):
    logging.info(request)
    q = db_session.query(User).filter(User.email == user['email']).one_or_none()
    logging.info(q)
    if q:
        if pbkdf2_sha256.verify(user['pwd'], q.pwd):
            return q.dump(), 200
        else:
            return NoContent, 401
    else:
        return NoContent, 404

def logout():
    session['user'] = None
    del session['user']
    return 200