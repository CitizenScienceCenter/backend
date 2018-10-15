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

db_session = orm_handler.db_session
ts = URLSafeTimedSerializer('SUPES_SECRET87').signer('SUPES_SECRET87')

def get_all(limit=20, search_term=None):
    q = db_session.query(User)
    print(search_term)
    if search_term:
        q = q.filter(User.email.match(search_term, postgresql_regconfig='english') | User.api_key.match(search_term, postgresql_regconfig='english') | User.id.match(search_term, postgresql_regconfig='english') | User.username.match(search_term, postgresql_regconfig='english'))
    return [u.dump() for u in q][:limit]

def get_one(id):
    # user = db_session.query(User).filter(User.email.match(id, postgresql_regconfig='english') | User.api_key.match(id, postgresql_regconfig='english') | User.id.match(id, postgresql_regconfig='english') | User.username.match(id, postgresql_regconfig='english')).one_or_none()
    user = db_session.query(User).filter(User.id == id).one_or_none()
    return user.dump() if user is not None else ('Not found', 404)

def post(user):
    logging.info('Creating user ')
    user['api_key'] = uuid.uuid4()
    user['pwd'] = pbkdf2_sha256.encrypt(user['pwd'], rounds=200000, salt_size=16)
    print(user)
    if ('username' in user and len(user['username']) == 0) or not 'username' in user:
        user['username'] = user['email']
    u = User(**user)
    try:
        db_session.add(u)
        db_session.commit()
        print(u.id)
        return u.dump(), 201
    except Exception as e:
        print(e)
        logging.error('User already registered or unrecoverable error occurred')
        return NoContent, 400
    
def put(id, user):
    q = db_session.query(User).filter(User.id == id).one_or_none()
    if q:
        for k in user:
            print(user[k])
            setattr(q, k, user[k])
        db_session.commit()
        print(q.id)
        return q.dump(), 201
    else:
        return NoContent, 404
