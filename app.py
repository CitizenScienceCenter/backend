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
from db.roles import RoleHandler
from minio import Minio
from middleware.response_handler import ResponseHandler


class Server:
    application = None
    app = None
    uploader = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.connexion_app = connexion.FlaskApp(__name__, specification_dir="./openapi")
        CORS(self.connexion_app.app)
        self.app = self.connexion_app.app
        if not os.environ.get("CC_ENV"):
            print("CC_ENV not set, using default (.env)")
            os.environ["CC_ENV"] = ".env"
        self.app.config.from_envvar("CC_ENV")
        self.connexion_app.add_api(
            self.connexion_app.app.config["OAPI_FILE"],
            strict_validation=False,
            validate_responses=False
        )
        self.config = self.app.config
        self.port = int(self.config["CC_PORT"]) or 9000
        self.debug = bool(self.config["DEBUG"]) or False
        self.app.secret_key = self.config["SECRET_KEY"] or uuid.uuid4()
        if self.config["ENV"] == "test" or self.config["ENV"] == "dev":
            try:
                DB.bind("sqlite", ":memory:")
            except BindingError as b:
                logging.error(b)
                pass
            else:
                DB.generate_mapping(create_tables=True)
        else:
            try:
                db_port = 5432
                if "PG_PORT" in self.config:
                    db_port = int(self.config["PG_PORT"])
                DB.bind(
                    provider="postgres",
                    user=self.config["PG_USER"],
                    password=self.config["PG_PASSWORD"],
                    hostaddr=self.config["PG_HOST"],
                    port=db_port,
                    database=self.config["PG_DB"],
                    sslmode="disable",
                )
                DB.generate_mapping(create_tables=True)
            except BindingError as e:
                logging.error(e)
                pass
            else:
                try:
                    DB.generate_mapping(create_tables=True)
                except Exception as e:
                    logging.error(e)
                    pass
        RoleHandler(DB).init_roles()
        Pony(self.connexion_app.app)
        print(self.config["ENV"])
        if self.config["ENV"] != "test" and self.config["ENV"] != "travis" and self.config["ENV"] != "dev":
            self.app.uploader = Minio(
                self.config["MIN_URL"],
                self.config["MIN_ACCESS"],
                self.config["MIN_SECRET"],
                self.config["MIN_SECURE"],
            )

        @self.connexion_app.app.errorhandler(401)
        def unauthorised_error(error):
            return ResponseHandler(
                401, "You do not have access to this object", body=str(error), ok=False
            ).send()

        @self.connexion_app.app.errorhandler(404)
        def not_found_error(error):
            return ResponseHandler(404, "Requested object not found", body=str(error), ok=False).send()

        @self.connexion_app.app.errorhandler(409)
        def conflict_error(error):
            return ResponseHandler(
                409, "Conflict occured, object already exists", body=error, ok=False
            ).send()

        @self.connexion_app.app.errorhandler(500)
        def internal_error(error):
            return ResponseHandler(
                500, "Internal server error", body=str(error), ok=False
            ).send()

    def run(self):
        if self.config["ENV"] in ["dev", "local", "test", "docker"]:
            logging.info("Running in Debug Mode")
            self.connexion_app.run(port=self.port, debug=True, threaded=True)
        else:
            self.connexion_app.run(port=self.port, debug=self.debug, server="gevent")


s = None

if __name__ == "__main__":
    s = Server()
    s.run()
