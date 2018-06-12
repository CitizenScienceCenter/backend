import connexion
from connexion import NoContent
from db import orm_handler, Submission, utils
from decorators import access_checks
from flask import request

db_session = orm_handler.db_session

def get(limit=20, search_term=None):
    q = db_session.query(Submission)
    if search_term:
        q = q.filter(Submission.name.match(search_term, postgresql_regconfig='english'))
    return [p.dump() for p in q][:limit]


def get_one(id=None):
    submission = db_session.query(Submission).filter(Submission.id == id).one_or_none()
    return submission.dump() if submission is not None else ('Not found', 404)

@access_checks.ensure_key
def create(submission):
    logging.info('Creating Submission ')
    print(submission)
    s = Submission(**submission)
    user = utils.get_user(request, db_session)
    s.user_id = user.id
    db_session.add(s)
    db_session.commit()
    return s.dump(), 201

@access_checks.ensure_key
def put(submission_id, submission):
    s = db_session.query(Submission).filter(Submission.id == submission_id).one_or_none()
    if s is not None:
        logging.info('Updating Submission %s..', submission_id)
        s.update(**submission)
    else:
        logging.info('Creating Submission %s..', submission_id)
        db_session.add(Submission(**submission))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)

@access_checks.ensure_key
def delete(submission_id):
    project = db_session.query(submission).filter(submission.id == submission_id).one_or_none()
    if project is not None:
        logging.info('Deleting Submission %s..', project_id)
        db_session.query(Submission).filter(submission.id == submission_id).delete()
        db_session.commit()
        return {msg: 'Deleted'}, 200
    else:
        return NoContent, 404