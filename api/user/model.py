import connexion
import uuid
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app
from decorators import access_checks
import json, smtplib
import email as emaillib
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from api import model
# from flask_sqlalchemy_session import current_session as db_session
from pony.flask import db_session
from pony.orm import *
from db import *

Model = User

allowed = ['username', 'pwd', 'email', 'info']

# @access_checks.ensure_model(Model)
@db_session
def get_users(limit=100, search_term=None):
    return None, 200

@access_checks.ensure_owner(Model)
def get_user(id=None):
    try:
        u = User[id]
        return {'msg': 'User found', 'user': u}, 200
    except core.ObjectNotFound:
        abort(404)

@db_session
def create_user(body):
    user = body
    print(body)
    user["api_key"] = uuid.uuid4()
    user["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(user["pwd"])
    if ("username" in user and len(user["username"]) == 0) or not "username" in user and "email" in user:
        user["username"] = user["email"].split("@")[0]
    u = User(**user)
    try:
        commit()
        return {'msg': 'User created', 'user': u.to_dict(exclude='pwd')}, 201
    except core.TransactionIntegrityError as e:
        return {'msg': 'User already exists', 'code': 401}
    if 'X-Api-Key' in request.headers and request.headers['X-Api-Key'] is not None:
        from_anon = request.headers['X-Api-Key']
        anon = User.select(lambda u: u.api_key == from_anon).first()
        if anon:
            print('deleting user')
            for s in User.submissions:
                s.user_id = u.id
            User.select(lambda u: u.id == anon_user.id).delete()
            db_session.commit()

@access_checks.ensure_user(Model)
def update_user(id, body):
    for k in body.keys():
        if k not in allowed:
            return {'msg': 'Edited property inaccessible', 'code': 401}, 401
    if 'pwd' in body:
        body["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(body["pwd"])
    
    m, code = model.put(Model, id, body)
    return m, code


@access_checks.ensure_user(Model)
@db_session
def delete_user(id):
    # user.relationship.clear() will empty all relations
    user = User[id].delete()
    commit()
    return {}, 200
