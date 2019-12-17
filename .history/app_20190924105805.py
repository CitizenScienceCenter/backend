#!/usr/bin/env python3
import datetime
import os
import logging
import uuid
import configparser
import connexion
from connexion.resolver import RestyResolver
from flask import session, request, g, app, jsonify
from pony.flask import Pony
from pony.orm import BindingError
from flask_cors import CORS
from db.models import DB
from middleware.response_handler import ResponseHandler

class Server:
    application = None
    app = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.connexion_app = connexion.FlaskApp(__name__, specification_dir="./openapi")
        CORS(self.connexion_app.app)
        self.app = self.connexion_app.app
        self.app.config.from_envvar('CC_ENV')
        self.connexion_app.add_api(self.connexion_app.app.config["SWAGGER_FILE"], options={'swagger_ui': False})

        self.port = int(self.connexion_app.app.config['CC_PORT']) or 8080
        self.debug = bool(self.connexion_app.app.config["DEBUG"]) or False

        self.config = self.app.config

        if self.config['ENV'] == 'local' or self.config['ENV'] == 'test':
            try:
                DB.bind('sqlite', ':memory:')
            except BindingError as b:
                logging.error(b)
                pass
            else:
                DB.generate_mapping(create_tables=True)
        else:
            try:
                DB.bind(
                    provider="postgres",
                    user=self.config['PG_USER'],
                    password=self.config['PG_PASSWORD'],
                    host=self.config['PG_HOST'],
                    database=self.config['PG_DB'],
                    sslmode='disable',
                )
            except BindingError as e:
                logging.error(e)
                pass
            else:
                try:
                    DB.generate_mapping(create_tables=True)
                except Exception as e:
                    logging.error(e)
                    pass

        self.connexion_app.app.secret_key = self.connexion_app.app.config["SECRET_KEY"] or uuid.uuid4()
        Pony(self.connexion_app.app)

        @self.connexion_app.app.errorhandler(401)
        def unauthorised_error(error):
            return ResponseHandler(401, 'You do not have access to this object', ok=False).send()

        @self.connexion_app.app.errorhandler(404)
        def not_found_error(error):
            return ResponseHandler(404, 'Requested object not found', ok=False).send()

        @self.connexion_app.app.errorhandler(409)
        def conflict_error(error):
            return ResponseHandler(409, 'Conflict occured, object already exists', ok=False).send()

        @self.connexion_app.app.errorhandler(500)
        def internal_error(error):
            return ResponseHandler(409, 'Internal server error', str(error), ok=False).send()

    def run(self):
        if self.connexion_app.app.config["ENV"] in ["dev", "local", "test", "docker"]:
            logging.info("Running in Debug Mode")
            self.connexion_app.run(port=self.port, debug=True, threaded=True)
        else:
            self.connexion_app.run(port=self.port, debug=self.debug, server="gevent")

s = None

if __name__ == "__main__":
    s = Server()
    s.run()
