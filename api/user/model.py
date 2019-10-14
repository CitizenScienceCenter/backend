import logging

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
from db import (
    DB,
    Activity,
    OToken,
    Project,
    Comment,
    Submission,
    Media,
    User,
    Task,
    utils,
)
from middleware.response_handler import ResponseHandler

Model = User

allowed = ["username", "pwd", "email", "info"]


@access_checks.ensure_model(Model)
@db_session
def get_users(limit=100, search_term=None, offset=0):
    return model.get_all(Model, limit, offset, search_term).send()


@db_session
def get_user():
    u = utils.get_user(request, db_session)
    return ResponseHandler(200, "User found", body=u.to_dict(exclude="pwd")).send()


@db_session
def create_user(body):
    user = body
    # user["api_key"] = uuid.uuid4()
    user["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(user["pwd"])
    if "anonymous" in user:
        if not user["anonymous"] and "email" not in user:
            return ResponseHandler(400, "Email is required", ok=False).send()
        if user["anonymous"] and not "username" in user:
            user["username"] = current_app.config["ANON_PREFIX"] + str(uuid.uuid4())
    res, u = model.post(User, user)
    res.set_val("data", u.to_dict(exclude="pwd"))
    if "X-Api-Key" in request.headers and request.headers["X-Api-Key"] is not None:
        from_anon = request.headers["X-Api-Key"]
        anon = User.get(api_key=from_anon)
        if anon:
            logging.warning("deleting anonymous user")
            for s in u.submissions:
                s.user_id = u.id
            User[anon_id].delete()
            commit()
    return res.send()


@db_session
@access_checks.ensure_owner
def update_user(body):
    current = utils.get_user(request, db_session)
    for k in body.keys():
        if k not in allowed:
            abort(401)
    if "pwd" in body:
        body["pwd"] = pbkdf2_sha256.using(rounds=200000, salt_size=16).hash(body["pwd"])

    res, u = model.put(Model, current, body)
    res.set_body(u.to_dict(exclude="pwd"))
    return res.send()


@db_session
@access_checks.ensure_owner
def delete_user():
    current = utils.get_user(request, db_session)
    current.delete()
    commit()
    # user.relationship.clear() will empty all relations
    return ResponseHandler(200, "User deleted").send()
