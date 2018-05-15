import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session
from db import orm_handler, User
from decorators import access_checks

db_session = orm_handler.init_db()

def get_users(limit, search_term=None):
    q = db_session.query(User)
    if search_term:
        q = q.filter(User.username == search_term)
    return [q.dump() for u in q][:limit]

def get(user_id):
    user = db_session.query(User).filter(User.user_id == user_id).one_or_none()
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

def login(user):
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
        
def register(user):
    logging.info('Creating user ')
    user['user_id'] = uuid.uuid4()
    user['api_key'] = uuid.uuid4()
    user['pwd'] = pbkdf2_sha256.encrypt(user['pwd'], rounds=200000, salt_size=16)
    user['created_at'] = datetime.utcnow()
    db_session.add(User(**user))
    db_session.commit()
    return user.dump(), 201

def login(user):
    print(user)
    q = db_session.query(User).filter(User.email == user['email']).one_or_none()
    logging.info(q)
    if q:
        if pbkdf2_sha256.verify(user['pwd'], q.pwd):
            return NoContent, 200
        else:
            return NoContent, 401
    else:
        return NoContent, 404

def logout():
    session['user'] = None
    del session['user']
    return 200