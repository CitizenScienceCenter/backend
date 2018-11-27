import connexion
import logging
import os, json
from connexion import NoContent
from db import orm_handler, Media, Activity, Task
from db.JTOS import jtos
from decorators import access_checks
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import uuid
from collections import namedtuple
from flask import send_file
import fleep
from pathlib import Path
import prison

db_session = orm_handler.db_session
js = jtos.JTOS()


@access_checks.ensure_model
def get_all(model, limit=25, search_term=None):
    if search_term:
        try:
            st = prison.loads(search_term)
            q_stmt = js.parseObject(st)
            print(q_stmt)
            res = db_session.execute(q_stmt)
            result_set = res.fetchall()
            records = result_set
            # records = [model(**r) for r in result_set]
            return [p for p in records][:limit], 200
        except Exception as e:
            # TODO handle parsing error
            print(e)
            return e
    q = db_session.query(model).all()
    return q, 200

def get_count(model, search_term=None):
    st = prison.loads(search_term)
    count_query = st.copy()
    count_query['select']['fields'] = ['COUNT(*)']
    if 'limit' in count_query:
        del count_query['limit']
    if 'offset' in count_query:
        del count_query['offset']
    count_stmt = js.parseObject(count_query)
    count = db_session.execute(count_stmt).fetchone()
    return count[0], 200

def get_one(model, id=None):
    m = db_session.query(model).filter(model.id == id).one_or_none()
    return m, 200 if m is not None else ("Not found", 404)


def get_file(model, id=None):
    m = db_session.query(model).filter(model.id == id).one_or_none()
    return send_file(m.path) if m is not None else ("Not found", 404)


def post(model, object):
    p = model(**object)
    print(p)
    try:
        db_session.add(p)
        db_session.commit()
        print(p.id)
        return p, 201
    except IntegrityError as ie:
        print(ie)
        return {"msg": "Resource already exists", "ok": False}, 409


def put(model, id, object):
    print(object)
    p = db_session.query(model).filter(model.id == id).one_or_none()
    print(p.dump())
    if "id" in object:
        del object["id"]
    if p is not None:
        logging.info("Updating %s %s..", model, id)
        for k in object.keys():
            setattr(p, k, object[k])
    else:
        logging.info("Creating object %s..", id)
        p = model(**object)
        db_session.add(p)
    db_session.commit()
    print(p.id)
    return p, (200 if p is not None else 201)


def delete(model, id):
    d = db_session.query(model).filter(model.id == id).one_or_none()
    if d is not None:
        logging.info("Deleting %s %s..", model, id)
        db_session.query(model).filter(model.id == id).delete()
        db_session.commit()
        return d.dump(), 200
    else:
        return NoContent, 404
