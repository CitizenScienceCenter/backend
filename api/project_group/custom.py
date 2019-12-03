import logging
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app, abort
from db import User, utils, Submission, Project, ProjectGroup
import smtplib
from email import message
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from decorators import access_checks
from middleware.response_handler import ResponseHandler

ts = URLSafeTimedSerializer("SUPES_SECRET87").signer("SUPES_SECRET87")
from pony.flask import db_session


@db_session
def get_project_group_projects(gid, limit=20, offset=0):
    p = ProjectGroup.get(id="{}".format(gid))
    if p and p.projects.count() > 0:
        return ResponseHandler(
            200,
            "",
            body=[s.to_dict() for s in p.projects.limit(limit, offset=offset)],
        ).send()
    elif p and p.projects.count() == 0:
        return ResponseHandler(
            200, "Project Group is empty", body=[], ok=False
        ).send()
    else:
        abort(404)

@db_session
def get_user_project_groups(limit=20, offset=0):
    u = utils.get_user(request, db_session)
    return ResponseHandler(200, "User Project Groups", body=[g.to_dict() for g in u.groups.limit(limit, offset=offset)]).send()
