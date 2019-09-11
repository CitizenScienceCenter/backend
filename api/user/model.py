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
from db import *

Model = User

# @access_checks.ensure_model(Model)
@db_session
def get_users(limit=100, search_term=None):
    ms, code =  model.get_all(Model, limit, search_term)
    u = User.select()
    print(u)
    if len(ms) > 0 and isinstance(ms[0], User):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code

@access_checks.ensure_owner(Model)
def get_user(id=None):
    m, code = model.get_one(Model, id)
    user = m.dump()
    del user['pwd']
    return user if m is not None else m, code

@db_session
def create_user(body):
    user = body
    print(body)
    user["api_key"] = uuid.uuid4()
    user["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(user["pwd"])
    if ("username" in user and len(user["username"]) == 0) or not "username" in user and "email" in user:
        user["username"] = user["email"].split("@")[0]

    u = User.get(username=user['username'], email=user['email'])
    if u is not None:
        return {'msg': 'User exists', 'code': 409}, 409
    else:
        try:
            u = User(**user)
            return {'msg': 'User created', 'user': u.to_dict()}, 200    
        except:
            return {'msg': 'Username or email already exists', 'code': 409}, 409
    # created_user, code = model.post(Model, user)
    # if 'X-Api-Key' in request.headers and request.headers['X-Api-Key'] is not None:
    #     from_anon = request.headers['X-Api-Key']
    #     anon = User.select(lambda u: u.api_key == from_anon).first()
    #     if anon:
    #         print('deleting user')
    #         db_session.execute("update submissions set user_id='{1}' where user_id='{0}'".format(anon_user.id, created_user.id))
    #         User.select(lambda u: u.id == anon_user.id).delete()
    #         db_session.commit()
    # if code == 201:
    #     if (created_user.info is not None and created_user.info['anonymous'] is False):
    #         user_project = {'name': created_user.username, 'description': 'Default space for {}'.format(created_user.username), 'active': True, 'owned_by': created_user.id}
    #         p = Project(**user_project)
    #         created_user.member_of.append(p)
    #         db_session.add(created_user)
    #         db_session.commit()
    #         db_session.refresh(created_user)
    #     return created_user.dump(), code
    # else:
    #     return created_user, 409



@access_checks.ensure_owner(Model)
def update_user(id, body):
    m, code = model.put(Model, id, body)
    return m.dump(), code


@access_checks.ensure_owner(Model)
@db_session
def delete_user(id):
    user = utils.get_user(request, db_session)
    user_projects = db_session.query(Project).filter(Project.owned_by == id).all()
    for p in user_projects:
        user.member_of.remove(p)
        p.owned_by = None # TODO handle the passing of this to a new user
        db_session.add(user)
        db_session.add(p)
    #     users = db_session.query(User).filter(User.member_of.any(Model.id==p.id)).all()
    #     for u in users:
    #         print(u.dump())
    #         u.member_of.remove(project)
    #         db_session.add(u)
        db_session.commit()
        # model.delete(Project, p.id)
    return model.delete(Model, id)
