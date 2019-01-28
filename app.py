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
        self.connexion_app = connexion.FlaskApp(__name__, specification_dir="./openapi/")

        env = DotEnv()
        env_loc = os.path.join(os.path.dirname(os.path.expanduser(os.path.expandvars(__file__))), '.env')
        env.init_app(self.connexion_app.app, env_file=env_loc, verbose_mode=False)

        self.connexion_app.add_api(self.connexion_app.app.config["SWAGGER_FILE"], options={'swagger_ui': False})

        self.port = int(self.connexion_app.app.config['CC_PORT']) or 8080
        self.debug = bool(self.connexion_app.app.config["DEBUG"]) or False

        self.connexion_app.app.secret_key = self.connexion_app.app.config["SECRET_KEY"] or uuid.uuid4()

        @self.connexion_app.app.after_request
        def apply_cors(response):
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, OPTIONS"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response

        @self.connexion_app.app.teardown_appcontext
        def shutdown_session(exception=None):
            orm_handler.db_session().remove()

    def run(self):
        if self.connexion_app.app.config["CC_ENV"] in ["dev", "local", "test", "docker"]:
            print("Running in Debug Mode")
            self.connexion_app.run(port=self.port, debug=True, threaded=True)
        else:
            self.connexion_app.run(port=self.port, debug=self.debug, server="gevent")


s = None

if __name__ == "__main__":
    s = Server()
    s.run()
