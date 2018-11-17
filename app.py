#!/usr/bin/env python3
import datetime
import os
import logging
import uuid
import configparser
import connexion
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template
from flask_cors import CORS
from flask_dotenv import DotEnv

from db import orm_handler

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__, static_url_path="./static")
app = connexion.App(__name__, specification_dir="./swagger/")
application = app.app
env = DotEnv()
env_loc = os.getenv('CC_ENV') or '.env'
env.init_app(application, env_file=env_loc, verbose_mode=False)
db_session = None
if "test" in application.config["CC_ENV"]:
    db_session = orm_handler.init_db(application.config["DB_URI"], persist=False)
else:
    db_session = orm_handler.init_db(application.config["DB_URI"], persist=True)
app.add_api(application.config["SWAGGER_FILE"], resolver=RestyResolver("api"))

application.secret_key = application.config["SECRET_KEY"] or uuid.uuid4()
CORS(application)


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


port = application.config["PORT"] or 8080
debug = application.config["DEBUG"] or False

if __name__ == "__main__":
    if (
        "dev" in application.config["CC_ENV"]
        or "local" in application.config["CC_ENV"]
        or "test" in application.config["CC_ENV"]
    ):
        print("Running in Debug Mode")
        app.run(port=port, debug=True)
    else:
        app.run(port=port, debug=debug, server="gevent")
