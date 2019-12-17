import connexion
import uuid
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app, abort
from decorators import access_checks
import json
import email as emaillib
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from api import model
from pony.flask import db_session
from pony.orm import core, commit
from db import DB, Activity, OToken, Project, Comment, Submission, Media, User, Task
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
    if 'anonymous' in user:
        if not user['anonymous'] and 'email' not in user:
            return ResponseHandler(400, 'Email is required', ok=False).send()
        if user['anonymous']:
            user['username'] = current_app.config['ANON_PREFIX'] + str(uuid.uuid4())
        
    res, u = model.post(User, user)
    res.set_body(u.to_dict(exclude='pwd'))
    if 'X-Api-Key' in request.headers and request.headers['X-Api-Key'] is not None:
        from_anon = request.headers['X-Api-Key']
        anon = User.get(api_key=from_anon)
        if anon:
            print('deleting anonymous user')
            for s in u.submissions:
                s.user_id = u.id
            User.get(id=anon.id).delete()
            commit()
    return res.send()

def update_user(id, body):
    for k in body.keys():
        if k not in allowed:
            abort(401)
    if 'pwd' in body:
        body["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(body["pwd"])
    
    res, u = model.put(Model, id, body)
    res.set_body(u.to_dict(exclude='pwd'))
    return res.send()


@db_session
def delete_user(id):
    # user.relationship.clear() will empty all relations
    return model.delete(User, id).send()
