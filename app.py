#!/usr/bin/env python3
import datetime
import logging
import uuid

import connexion
from connexion import NoContent
from connexion.resolver import RestyResolver

import orm

db_session = None

logging.basicConfig(level=logging.INFO)
db_session = orm.init_db('postgresql://pybossa:tester@localhost/cccs')
app = connexion.FlaskApp(__name__)
app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('swagger.yaml', resolver=RestyResolver('api'))

application = app.app

@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=8080, debug=True)
