import logging

import prison
from connexion import NoContent
from flask import send_file, abort
from jtos import jtos
from sqlalchemy.exc import IntegrityError
from pony.orm import core, commit, select
from db import DB, User, Project, Task, Member, Submission, Comment, Media
from decorators import access_checks
from datetime import datetime
import uuid
from middleware.response_handler import ResponseHandler

from pony.flask import db_session

js = jtos.JTOS()


@db_session
def get_all(model, limit, offset, search_term=None):
    """
        Get an array of all types of a model, can use JTOS query handling to turn JSON to SQL and search
    """
    r = ResponseHandler(200, "")
    r.set_val("page", {"limit": limit, "offset": offset})
    if search_term:
        try:
            st = prison.loads(search_term)
            if "limit" not in st.keys():
                st["limit"] = 20
            if "offset" not in st.keys():
                st["offset"] = 0
            q_stmt = js.parse_object(st)
            logging.info(q_stmt)
            q = model.select_by_sql(q_stmt)
        except Exception as e:
            logging.error(e)
            abort(500, "Failed to understand query")
    else:
        q = select(a for a in model).limit(limit, offset=offset)
    q = [o.to_dict() for o in q]
    r.set_body(q)
    return r

@db_session
def get_one(model, id=None):
    """
        Retrieve a model based on the ID
    """
    try:
        m = model[id]
    except core.ObjectNotFound:
        abort(404)
    return ResponseHandler(200, "Object found", body=m.to_dict())


@db_session
def get_file(model, id=None):
    m = model[id]
    return send_file(m.path) if m is not None else m, 404


@db_session
def post(model, obj):
    """
        Create a model from provided params. Connexion handles the validation
    """
    obj['id'] = uuid.uuid4()
    p = model(**obj)
    print(p.to_dict())
    try:
        commit()
        obj = model.__name__.lower()
        # use model.__name__.lower() for class name
    except Exception as e:
        print(e)
        abort(500, str(e))
    return ResponseHandler(201, "{} created".format(obj), body=p.to_dict()), p


@db_session
def put(model, id, object):
    """
        Update a model from provided ID and params
    """
    try:
        p = model[id]
    except core.ObjectNotFound as o:
        logging.error(o)
        abort(404)
    if "id" in object:
        del object["id"]
    logging.info("Updating %s %s..", model, id)
    for k in object.keys():
        setattr(p, k, object[k])
    object['updated_at'] = datetime.now()
    try:
        commit()
    except Exception as e:
        abort(500, str(e))
    obj = model.__name__.lower()
    return ResponseHandler(201, "{} updated".format(obj), body=p.to_dict()), p


@db_session
def delete(model, id):
    """
        Delete a model based on the ID.
        Individual instances handle access checks
    """
    try:
        model[id].delete()
        commit()
    except Exception as e:
        logging.error(e)
        abort(500)
    obj = model.__name__.lower()
    return ResponseHandler(200, "{} deleted".format(obj))
