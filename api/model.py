import logging

import prison
from connexion import NoContent
from flask import send_file, abort
from jtos import jtos
from sqlalchemy.exc import IntegrityError
from pony.orm import *
from db import orm_handler
from decorators import access_checks

# from flask_sqlalchemy_session import current_session as db_session

from pony.flask import db_session
js = jtos.JTOS()

@access_checks.ensure_model
@db_session
def get_all(model, limit=25, search_term=None):
    if search_term:
        try:
            print(search_term)
            st = prison.loads(search_term)
            q_stmt = js.parse_object(st)
            print("SQL: ", q_stmt)
            res = db_session.execute(q_stmt)
            result_set = res.fetchall()
            records = result_set
            # records = [model(**r) for r in result_set]
            return [p for p in records][:limit], 200
        except Exception as e:
            # TODO handle parsing error
            print("Search failed", e)
            abort(500)
    q = db_session.query(model).all()
    # db_session().close()
    return q, 200

@db_session
def get_count(model, search_term=None):
    st = prison.loads(search_term)
    count_query = st.copy()
    count_query['select']['fields'] = ['COUNT(*)']
    if 'limit' in count_query:
        del count_query['limit']
    if 'offset' in count_query:
        del count_query['offset']
    count_stmt = js.parse_object(count_query)
    count = db_session.execute(count_stmt).fetchone()
    # db_session().close()
    return count[0], 200

@db_session
def get_one(model, id=None):
    m = db_session.query(model).filter(model.id == id).one_or_none()
    # db_session().close()
    return (m, 200) if m is not None else (m, 404)

@db_session
def get_file(model, id=None):
    m = db_session.query(model).filter(model.id == id).one_or_none()
    # db_session().close()
    return send_file(m.path) if m is not None else m, 404

@db_session
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
        abort(409)

@db_session
def put(model, id, object):
    try:
        p = model[id]
    except core.ObjectNotFound as o:
        return {'msg': 'Requested object not found', 'code': 404}, 404
    if "id" in object:
        del object["id"]
    logging.info("Updating %s %s..", model, id)
    for k in object.keys():
        setattr(p, k, object[k])
    commit()
    return {'msg': 'User updated', 'code': 200, 'user': p.to_dict(exclude='pwd')}, 200

@db_session
def delete(model, id):
    d = db_session.query(model).filter(model.id == id).one_or_none()
    if d is not None:
        logging.info("Deleting %s %s..", model, id)
        db_session.query(model).filter(model.id == id).delete()
        db_session.commit()
        return d.dump(), 200
    else:
        abort(404)
