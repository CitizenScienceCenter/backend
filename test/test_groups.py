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

def test_delete_groups(client):
    user = utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)
    groups = utils.get_groups(client, user['api_key'])
    for g in groups:
        lg = client.delete('/api/v1/groups/{0}'.format(g['id']), headers=[('X-API-KEY', user['api_key'])])
        assert lg.status_code == 200

def test_create_groups(client):
    user = utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)
    lg = client.post('/api/v1/groups', json={'name': 'Test Group', 'description': 'A Test Group'}, headers=[('X-API-KEY', user['api_key'])])
    assert lg.status_code == 201
    test_delete_groups(client)

def test_create_groups__invalid(client):
    user = utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)
    lg = client.post('/api/v1/groups', json={}, headers=[('X-API-KEY', user['api_key'])])
    assert lg.status_code == 400
