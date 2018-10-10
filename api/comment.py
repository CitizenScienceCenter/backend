import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils
from decorators import access_checks
from flask import request
import logging

db_session = orm_handler.db_session

def get_comments(limit=20, search_term=None):
    q = db_session.query(Comment)
    if search_term:
        q = q.filter(Comment.content.match(search_term, postgresql_regconfig='english'))
    return [p.dump() for p in q][:limit]


def get_comment(id=None):
    comment = db_session.query(Comment).filter(Comment.id == id).one_or_none()
    return comment.dump() if commment is not None else ('Not found', 404)

@access_checks.ensure_key
def create_comment(comment):
    logging.info('Creating Comment ')
    s = Comment(**comment)
    # user = utils.get_user(request, db_session)
    # s.user_id = user.id
    db_session.add(s)
    db_session.commit()
    print(s.id)
    return s.dump(), 201

@access_checks.ensure_key
def put_comment(comment_id, comment):
    s = db_session.query(Comment).filter(Comment.id == comment_id).one_or_none()
    if s is not None:
        logging.info('Updating comment %s..', comment_id)
        s.update(**submission)
    else:
        logging.info('Creating comment %s..', comment_id)
        s = Comment(**comment)
        db_session.add(s)
    db_session.commit()
    return s.dump(), (200 if s is not None else 201)

@access_checks.ensure_key
def delete_comment(comment_id):
    comment = db_session.query(Submission).filter(submission.id == submission_id).one_or_none()
    if comment is not None:
        logging.info('Deleting Comment %s..', comment_id)
        db_session.query(Comment).filter(Comment.id == comment_id).delete()
        db_session.commit()
        return {msg: 'Deleted'}, 200
    else:
        return NoContent, 404