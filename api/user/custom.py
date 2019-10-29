import logging
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app, abort
from db import User, utils, Submission
import smtplib
from email import message
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from pony.orm import commit
from middleware.response_handler import ResponseHandler


ts = URLSafeTimedSerializer("SUPES_SECRET87").signer("SUPES_SECRET87")
from pony.flask import db_session


@db_session
def validate(key):
    return utils.get_user(request, db_session).to_dict(exclude="pwd")


@db_session
def login(body):
    logging.info(request)
    q = None
    user = body
    if "email" in user:
        q = User.get(email=user["email"])
        logging.info(q)
    elif "username" in user:
        q = User.get(username=user["username"])
    else:
        return {"msg": "Incorrect keys provided"}, 500
    if q:
        if pbkdf2_sha256.verify(user["pwd"], q.pwd):
            return ResponseHandler(200, 'Welcome', body=q.to_dict(exclude="pwd")).send()
        else:
            abort(401)
    else:
        return {"msg": "User not found"}, 404


def logout():
    session["user"] = None
    del session["user"]
    return 200


@db_session
def auth(body):
    user = body
    # TODO create oauth token here and add to table. Just send api key for now
    q = User.get(email=user["email"])
    if q:
        if pbkdf2_sha256.verify(user["pwd"], q.pwd):
            session["user"] = q.dump()
            return q.dump(), 200
        else:
            return NoContent, 401
    else:
        return NoContent, 404


@db_session
def reset(email):
    conf = current_app.config
    user = User.get(email=email)
    # TODO handle domain
    if user:
        tk = ts.sign(str(user.id))
        reset = "{}/reset/{}".format("https://citizenscience.ch", tk.decode("utf-8"))
        text = "Hello! \n Someone requested a password for your account. Please click the link {} to change it. \n Thanks, The Citizen Science Team".format(
            reset
        )
        msg = message.EmailMessage()
        msg.set_content(text)
        smtp_user = conf["SMTP_USER"]
        msg["Subject"] = "Password Reset for Citizen Science Project"
        msg["From"] = smtp_user
        msg["To"] = user.email
        try:
            s = smtplib.SMTP(conf["SMTP_ADDR"], 587)
            s.login(smtp_user, conf["SMTP_PASS"])
            s.sendmail(smtp_user, [user.email], msg.as_string())
            s.quit()
        except Exception as e:
            logging.error(e)
            abort(501)
        return NoContent, 200
    else:
        abort(404)


@db_session
def get_user_submissions():
    user = utils.get_user(request, db_session)
    submissions = user.submissions
    if submissions.count() > 0:
        return ResponseHandler(200, '', body=[s.to_dict() for s in submissions]).send()
    else:
        return ResponseHandler(200, 'User has no submissions', body=[], ok=False).send()


@db_session
def verify_reset(reset):
    logging.debug(reset)
    try:
        # TODO check token signature
        token = ts.unsign(reset["token"], 2000)
        logging.info(token)
        user = User.get(id=reset["id"])
        if user:
            user.pwd = pbkdf2_sha256.encrypt(reset["pwd"], rounds=200000, salt_size=16)
            commit()
        else:
            abort(404)
        return True, 200
    except Exception as e:
        logging.error(e)
        abort(401)
