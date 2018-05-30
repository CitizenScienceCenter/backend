import connexion
from connexion import NoContent
from db import orm_handler, Media
from decorators import access_checks

db_session = orm_handler.db_session

def get(limit, search_term=None):
    q = db_session.query(Submission)
    if search_term:
        q = q.filter(Submission.name == search_term)
    return [p.dump() for p in q][:limit]


def get_one(id=None):
    submission = db_session.query(Media).filter(Submission.id == id).one_or_none()
    return submission.dump() if submission is not None else ('Not found', 404)

@access_checks.ensure_key
def create(media):
    logging.info('Creating Media ')
    attachment = connexion.request.files['attachment']
    # TODO save file here
    db_session.add(Media(**media))
    db_session.commit()
    return NoContent, 201

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