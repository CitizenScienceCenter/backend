#!/usr/bin/env python3
import datetime
import logging
import uuid

import connexion
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template
from flask_cors import CORS

from db import orm_handler

import config

db_session = None

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__)
app = connexion.App(__name__, specification_dir=config.SWAGGER_DIR)
db_session = orm_handler.init_db()
app.add_api('swagger.yaml', resolver=RestyResolver('api'))

application = app.app
application.secret_key = config.SECRET_KEY or uuid.uuid4()
CORS(application)

# @application.route('/oauth/authorize')
# def auth():
#     # TODO implement login page example (or remove since this is extraneous to API)
#     return render_template('index.html')


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

port = config.PORT or 8080
debug = config.DEBUG or False

if __name__ == '__main__':
    app.run(port=port, debug=debug)
