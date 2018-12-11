import connexion
import logging
import os
from connexion import NoContent
from db import orm_handler, Media
from decorators import access_checks
from werkzeug.utils import secure_filename
import uuid
from flask import send_file
import fleep
from pathlib import Path

db_session = orm_handler.db_session


def get_for_source(id=None, limit=20):
    m = db_session().query(Media).filter(Media.source_id == id)
    return [p.dump() for p in m][:limit]

def upload(attachment, id=None):
    logging.info("Creating Media ")
    f = connexion.request.files["attachment"]
    filename = secure_filename(f.filename)
    uid = uuid.uuid4().hex
    ext = Path(f.filename).suffix
    path = "./static/uploads/{}{}".format(uid, ext)
    f.save(path)
    with open(path, "rb") as f:
        info = fleep.get(f.read(128))
    print(info.type)
    m = Media(id, path, filename, info.type[0])
    # name = os.path.basename(path)
    db_session().add(m)
    db_session().commit()
    print(m.id)
    return m.dump(), 201
