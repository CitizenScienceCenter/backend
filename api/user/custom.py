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
from email import message
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
# from flask_sqlalchemy_session import current_session as db_session
db_session = orm_handler.db_session
ts = URLSafeTimedSerializer("SUPES_SECRET87").signer("SUPES_SECRET87")


def validate(key):
    q = db_session.query(User).filter(User.api_key == key).one_or_none()
    if q:
        return q.dump(), 201
    else:
        return NoContent, 401


def login(user):
    logging.info(request)
    q = None
    # user = body
    # print(body)
    if 'email' in user:
        q = db_session.query(User).filter(User.email == user["email"]).one_or_none()
        logging.info(q)
    elif 'username' in user:
        q = db_session.query(User).filter(User.username == user["username"]).one_or_none()
    else:
        return {'msg': 'Incorrect keys provided'}, 500
    if q:
        if pbkdf2_sha256.verify(user["pwd"], q.pwd):
            del q.pwd
            return q.dump(), 200
        else:
            return NoContent, 401
    else:
        return {'msg': 'User not found'}, 404


def logout():
    session["user"] = None
    del session["user"]
    return 200


def auth(user):
    # TODO create oauth token here and add to table. Just send api key for now
    q = db_session.query(User).filter(User.email == user["email"]).one_or_none()
    if q:
        if pbkdf2_sha256.verify(user["pwd"], q.pwd):
            session["user"] = q.dump()
            return q.dump(), 200
        else:
            return NoContent, 401
    else:
        return NoContent, 404


def reset(email):
    conf = current_app.config
    user = (
        db_session.query(User)
        .filter(User.email != None)
        .filter(User.email == email)
        .one_or_none()
    )
    if user:
        tk = ts.sign(user.id)
        reset = "{}/reset/{}".format("https://snakes.citizenscience.ch", tk.decode("utf-8"))
        text = "Hello! \n Someone requested a password for your account. Please click the link {} to change it. \n Thanks, The Citizen Science Team".format(
            reset
        )
        msg = message.EmailMessage()
        msg.set_content(text)
        smtp_user = "info@citizenscience.ch"
        msg["Subject"] = "Password Reset for Citizen Science Project"
        msg["From"] = smtp_user
        msg["To"] = user.email
        try:
            s = smtplib.SMTP("asmtp.mailstation.ch", 587)
            s.login(smtp_user, "UniZuETH2018")
            s.sendmail(smtp_user, [user.email], msg.as_string())
            s.quit()
        except Exception as e:
            print("ERROR RESETTING", e)
            return e, 503
        return NoContent, 200
    else:
        return NoContent, 401


def get_subs(id=None):
    user = db_session.query(User).filter(User.id == id).one_or_none()
    if user:
        submissions = (
            db_session.query(Submission)
            .distinct(Submission.id)
            .filter(Submission.user_id == id)
            .all()
        )
        # TODO paging
        return [s.dump() for s in submissions]
    else:
        return NoContent, 401


def verify_reset(reset):
    print(reset)
    try:
        token = ts.unsign(reset["token"], 2000)
        user = db_session.query(User).filter(User.id == reset["id"]).one_or_none()
        user.pwd = pbkdf2_sha256.encrypt(reset["pwd"], rounds=200000, salt_size=16)
        db_session.commit()
        return True, 200
    except Exception as e:
        print(e)
        return False, 401
