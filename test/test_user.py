import pytest
import uuid
import configparser
import connexion
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template
from flask_cors import CORS

from db import orm_handler

from app import app

from test import t_con


@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as c:
        yield c

def test_register(client):
    lg = client.post('/api/v1/users/register', json={
        'email': t_con.TEST_USER, 'pwd': t_con.TEST_PWD
    })
    assert lg.status_code == 201 or lg.status_code == 409

def test_login(client):
    lg = client.post('/api/v1/users/login', json={
        'email': t_con.TEST_USER, 'pwd': t_con.TEST_PWD
    })
    print(lg.data)
    assert lg.status_code == 200
