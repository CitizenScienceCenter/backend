import logging
from datetime import datetime
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session, request, current_app, abort
from db import User, utils, Submission, Project, Activity
import smtplib
from email import message
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from decorators import access_checks
from middleware.response_handler import ResponseHandler

ts = URLSafeTimedSerializer("SUPES_SECRET87").signer("SUPES_SECRET87")
from pony.flask import db_session


@db_session
@access_checks.ensure_owner(Project)
def get_project_submissions(id=None, limit=20, offset=0):
    p = Project.get(id=id)
    if p:
        return [s.to_dict() for s in p.submissions.limit(limit, offset=offset)]
    else:
        abort(404)


@db_session
def get_project_activities(id=None, limit=20, offset=0):
    p = Project.get(id=id)
    if p and p.activities.count() > 0:
        return ResponseHandler(
            200,
            "",
            body=[s.to_dict() for s in p.activities.limit(limit, offset=offset)],
        ).send()
    elif a and a.submissions.count() == 0:
        return ResponseHandler(
            200, "Project has no activities", body=[], ok=False
        ).send()
    else:
        abort(404)


@db_session
def get_project_taskss(id=None, limit=20, offset=0):
    p = Project.get(id=id)
    if p and p.tasks.count() > 0:
        return [s.to_dict() for s in p.tasks.limit(limit, offset=offset)]
    elif p and p.tasks.count() > 0:
        return ResponseHandler(200, "Project has no tasks", body=[], ok=False).send()
    else:
        abort(404)
