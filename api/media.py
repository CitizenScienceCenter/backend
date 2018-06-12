import connexion
import logging
import os
from connexion import NoContent
from db import orm_handler, Media
from decorators import access_checks
from werkzeug.utils import secure_filename
from flask import send_file

db_session = orm_handler.db_session

def get(limit=20, search_term=None):
    q = db_session.query(Media)
    if search_term:
        q = q.filter(Media.id.match(search_term, postgresql_regconfig='english') | Media.path.match(search_term, postgresql_regconfig='english'))
    return [p.dump() for p in q][:limit]


def get_one(id=None):
    m = db_session.query(Media).filter(Media.id == id).one_or_none()
    print(m)
    return send_file(m.path) if m is not None else ('Not found', 404)

@access_checks.ensure_key
def upload(id, attachment):
    logging.info('Creating Media ')
    f = connexion.request.files['attachment']
    filename = secure_filename(f.filename)
    path = os.path.join('./static/uploads/', '{}_{}'.format(id, filename))
    f.save(path)
    m = Media(id, path)
    db_session.add(m)
    db_session.commit()
    return NoContent, 201

@access_checks.ensure_key
def put(id, media):
    s = db_session.query(Media).filter(Media.id == id).one_or_none()
    if s is not None:
        logging.info('Updating Submission %s..', id)
        s.update(**submission)
    else:
        logging.info('Creating Submission %s..', id)
        db_session.add(Media(**media))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)

@access_checks.ensure_key
def delete(id):
    project = db_session.query(Media).filter(Media.id == id).one_or_none()
    if project is not None:
        logging.info('Deleting Submission %s..', id)
        db_session.query(Media).filter(Media.id == id).delete()
        db_session.commit()
        return {msg: 'Deleted'}, 200
    else:
        return NoContent, 404