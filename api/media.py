import connexion
import logging
import os
from connexion import NoContent
from db import orm_handler, Media
from decorators import access_checks
from werkzeug.utils import secure_filename
from flask import send_file
import fleep

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
    with open(path, "rb") as f:
        info = fleep.get(f.read(128))
    print(info.type)
    name = os.path.basename(path)
    m = Media(id, path, info.type[0], name)
    db_session.add(m)
    db_session.commit()
    return NoContent, 201

@access_checks.ensure_key
def put(id, media):
    s = db_session.query(Media).filter(Media.id == id).one_or_none()
    if s is not None:
        logging.info('Updating Media %s..', id)
        s.update(**submission)
    else:
        logging.info('Creating Media %s..', id)
        db_session.add(Media(**media))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)

@access_checks.ensure_key
def delete(id):
    media = db_session.query(Media).filter(Media.id == id).one_or_none()
    if media is not None:
        logging.info('Deleting Media %s..', id)
        os.remove(media.path)
        db_session.query(Media).filter(Media.id == id).delete()
        db_session.commit()
        return media.dump(), 200
    else:
        return NoContent, 404
