import connexion
import logging
import uuid
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app
from db import orm_handler, User, utils, Submission, Project
from decorators import access_checks
import json, smtplib
import email as emaillib
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from api import model
from api.project import model as ProjectAPI

db_session = orm_handler.db_session()

Model = User

def get_users(limit=100, search_term=None):
    ms, code =  model.get_all(Model, limit, search_term)
    if len(ms) > 0 and isinstance(ms[0], User):
        return [m.dump() for m in ms][:limit], code
    else:
        return [dict(m) for m in ms][:limit], code

@access_checks.ensure_owner(Model)
def get_user(id=None):
    m, code = model.get_one(Model, id)
    return m.dump() if m is not None else m, code


def create_user(user):
    user["api_key"] = uuid.uuid4()
    user["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(user["pwd"])
    if ("username" in user and len(user["username"]) == 0) or not "username" in user:
        user["username"] = user["email"].split("@")[0]
    created_user, code = model.post(Model, user)
    if 'X-Api-Key' in request.headers and request.headers['X-Api-Key'] is not None:
        from_anon = request.headers['X-Api-Key']
        anon_user = db_session().query(User).filter(User.api_key == from_anon).one_or_none()
        if anon_user:
            print('deleting user')
            db_session.execute("update submissions set user_id='{1}' where user_id='{0}'".format(anon_user.id, created_user.id))
            db_session().query(User).filter(User.id == anon_user.id).delete()
            db_session.commit()
    if isinstance(created_user, Model):
        if (created_user.info is not None and created_user.info['anonymous'] is False):
            user_project = {'name': created_user.username, 'description': 'Default space for {}'.format(created_user.username), 'active': True, 'owned_by': created_user.id}
            p = Project(**user_project)
            created_user.member_of.append(p)
            db_session.add(created_user)
            db_session.commit()
            db_session.refresh(created_user)
        return created_user.dump(), code
    else:
        return created_user, 409



@access_checks.ensure_owner(Model)
def update_user(id, user):
    m, code = model.put(Model, id, request.get_json())
    return m.dump(), code


@access_checks.ensure_owner(Model)
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
