import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app
from db import orm_handler, User, utils
from decorators import access_checks
import json, smtplib, email 
from itsdangerous import TimestampSigner

db_session = orm_handler.db_session
ts = TimestampSigner('SUPES_SECRET87')

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

def reset(id):
    tk = ts.sign(id)
    conf = current_app.config
    user = utils.get_user(request, db_session)
    reset = "wenker.citizenscience.ch/reset?token={}".format(tk)
    message = "Hello! \n Someone requested a password for your account. Please click the link {} to change it. \n Thanks, The Citizen Science Team".format("reset")
    msg = email.message.EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Password Reset for Citizen Science Wenker Project'
    msg['From'] = conf['SMTP_USER']
    msg['To'] = user.email or None
    s = smtplib.SMTP(conf['SMTP_ADDR'], conf['SMTP_PORT'])
    s.login(conf['SMTP_USER'], conf['SMTP_PASS'])
    s.sendmail(me, [you], msg)
    s.quit()
    # TODO send email here
    return {'token': tk}, 200


def verify(token):
    try:
        token = ts.unsign(token, 120)
        return True, 200
    except Exception:
        return False, 301

def register_user(user):
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
    
def update_user(id, user):
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
