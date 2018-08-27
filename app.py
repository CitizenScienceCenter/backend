#!/usr/bin/env python3
import datetime
import logging
import uuid
import configparser
import connexion
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template
from flask_cors import CORS

from db import orm_handler

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__, static_url_path='static/')
app = connexion.App(__name__, specification_dir='swagger/')
application = app.app
application.config.from_envvar('CC_ENV')
db_session = orm_handler.init_db(application.config['DB_URI'], persist=False)
app.add_api(application.config['SWAGGER_FILE'], resolver=RestyResolver('api'))

application.secret_key = application.config['SECRET_KEY'] or uuid.uuid4()
CORS(application)

@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

port = application.config['PORT'] or 8080
debug = application.config['DEBUG'] or False

if __name__ == '__main__':
    app.run(port=port, debug=debug)
