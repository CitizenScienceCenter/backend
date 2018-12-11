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

class Server:
    application = None
    app = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        app = connexion.FlaskApp(__name__)
        self.app = connexion.App(__name__, specification_dir="./swagger/")
        self.application = app.app
        env = DotEnv()
        env_loc = os.path.join(os.path.dirname(os.path.expanduser(os.path.expandvars(__file__))), '.env')
        env.init_app(self.application, env_file=env_loc, verbose_mode=False)
        self.port = int(self.application.config['PORT']) or 8080
        self.debug = self.application.config["DEBUG"] or False
        self.app.add_api(self.application.config["SWAGGER_FILE"], options={'swagger_ui': False})
        self.application.secret_key = self.application.config["SECRET_KEY"] or uuid.uuid4()
        CORS(self.application)

        @self.application.teardown_appcontext
        def shutdown_session(exception=None):
            orm_handler.db_session().remove()

    def run(self):
        if self.application.config["CC_ENV"] in ["dev", "local", "test", "docker"]:
            print("Running in Debug Mode")
            self.app.run(port=self.port, debug=True)
        else:
            self.app.run(port=self.port, debug=self.debug, server="gevent")

if __name__ == "__main__":
    s = Server()
    s.run()
