import connexion
import logging
import os
from connexion import NoContent
from db import orm_handler, Media
from decorators import access_checks
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import uuid
from flask import send_file
import fleep
from pathlib import Path

db_session = orm_handler.db_session

def get_all(model, limit, search_term):
    q = db_session.query(model)
    # if search_term:
    #     q = q.filter(model.source_id == search_term)
    return [p.dump() for p in q][:limit]


def get_one(model, id=None):
    m = db_session.query(model).filter(model.id == id).one_or_none()
    return m.dump() if m is not None else ('Not found', 404)

def get_file(model, id=None):
    m = db_session.query(model).filter(model.id == id).one_or_none()
    return send_file(m.path) if m is not None else ('Not found', 404)

def post(model, object):
    p = model(**object)
    try:
        db_session.add(p)
        db_session.commit()
        print(p.id)
        return p.dump(), 201
    except IntegrityError as ie:
        return {'msg': 'Resource already exists', 'ok': False}, 409

@access_checks.ensure_key
def put(model, id, object):
    p = db_session.query(model).filter(model.id == id).one_or_none()
    print(p.dump())
    if 'id' in object:
        del object['id']
    if p is not None:
        logging.info('Updating %s %s..', model, id)
        for k in object.keys():
            setattr(p, k, object[k])
    else:
        logging.info('Creating object %s..', id)
        p = model(**object)
        db_session.add(p)
    db_session.commit()
    print(p.id)
    return p.dump(), (200 if p is not None else 201)

@access_checks.ensure_key
def delete(model, id):
    d = db_session.query(model).filter(model.id == id).one_or_none()
    if d is not None:
        logging.info('Deleting %s %s..', model, id)
        db_session.query(model).filter(model.id == id).delete()
        db_session.commit()
        return d.dump(), 200
    else:
        return NoContent, 404
