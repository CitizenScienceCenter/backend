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
from pony.flask import db_session
from pony.orm import *
from db import *
from middleware.response_handler import ResponseHandler

Model = User

allowed = ['username', 'pwd', 'email', 'info']

@access_checks.ensure_model(Model)
@db_session
def get_users(limit=100, search_term=None, offset=0):
    return model.get_all(Model, limit, offset, search_term).send()

@access_checks.ensure_owner(Model)
def get_user(id=None):
    try:
        u = User[id]
        return ResponseHandler(200, 'User found', body=u.to_dict(exclude='pwd')).send()
    except core.ObjectNotFound:
        abort(404)

@db_session
def create_user(body):
    user = body
    user["api_key"] = uuid.uuid4()
    user["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(user["pwd"])
    if ("username" in user and len(user["username"]) == 0) or not "username" in user and "email" in user:
        user["username"] = user["email"].split("@")[0]
    res, u = model.post(User, user)
    res.set_body(u.to_dict(exclude='pwd'))
    if 'X-Api-Key' in request.headers and request.headers['X-Api-Key'] is not None:
        from_anon = request.headers['X-Api-Key']
        anon = User.get(api_key=from_anon)
        print(anon)
        if anon:
            print('deleting user')
            for s in u.submissions:
                s.user_id = u.id
            User.get(id=anon.id).delete()
            commit()
    return res.send()

def update_user(id, body):
    for k in body.keys():
        if k not in allowed:
            return {'msg': 'Edited property inaccessible', 'code': 401}, 401
    if 'pwd' in body:
        body["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(body["pwd"])
    
    res, u = model.put(Model, id, body)
    res.set_body(u.to_dict(exclude='pwd'))
    return res.send()


@db_session
def delete_user(id):
    # user.relationship.clear() will empty all relations
    return model.delete(User, id).send()
