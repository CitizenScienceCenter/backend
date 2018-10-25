import pytest
import uuid
import configparser
import connexion
import json
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template, Response
from flask_cors import CORS

from db import orm_handler

from app import app

from test import t_con, utils

@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as c:
        yield c

def test_create_groups(client):
    user = json.loads(utils.login(client, t_con.TEST_USER, t_con.TEST_PWD).get_data())
    print(user['api_key'])
    lg = client.post('/api/v1/groups', json={'name': 'Test Group'}, headers=[('X-API-KEY', user['api_key'])])
    print(lg.get_data())
    assert lg.status_code == 201
