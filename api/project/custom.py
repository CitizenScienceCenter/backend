import logging
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app
from db import User, utils, Submission, Project
import smtplib
from email import message
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from decorators import access_checks

ts = URLSafeTimedSerializer("SUPES_SECRET87").signer("SUPES_SECRET87")
from pony.flask import db_session

@db_session
@access_checks.ensure_owner(Project)
def get_project_submissions(id=None, limit=20, offset=0):
    user = utils.get_user(request, db_session)
    p = Project.get(id=id)
    if p:
        return [s.to_dict() for s in p.submissions]
    else:
        abort(404)