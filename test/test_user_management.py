import json

import pytest

from app import Server
from test import t_con, utils
from datetime import datetime
import hashlib
import time


anon_name = '_anon{}'.format('dfjkshfuihvuiehfnijvrifbvrf')
anon_pwd = 'sbdshf783yfh4ub47iwhiu9heiu' 

@pytest.fixture(scope="module")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c

@pytest.fixture(scope="module")
def anonymous_user(client):
    u = {
        'username': anon_name,
        'pwd': anon_pwd,
        'confirmed': False,
        'info': {
            'anonymous': True
        }
    }
    return client.post(
        "/api/v2/users/register", json=u
    )

@pytest.fixture(scope="module")
def login_anonymous(client, anonymous_user):
    lg = client.post(
        "/api/v2/users/login", json={"username": anon_name, "pwd": anon_pwd}
    )
    assert lg.status_code == 200
    user = json.loads(lg.data)
    assert 'pwd' not in user
    return user

@pytest.mark.third
def test_convert_anonymous_user(client, login_anonymous):
    lg = client.post(
        "/api/v2/users/register", json={"email": 'abc@abc.com', "pwd": 'dklfjfkf373'},
        headers=[("X-API-KEY", login_anonymous['api_key'])],
    )
    assert lg.status_code == 201

@pytest.mark.fourth
def test_anonymous_fail(client):
    lg = client.post(
        "/api/v2/users/login", json={"username": anon_name, "pwd": anon_pwd},
    )
    assert lg.status_code == 404

@pytest.mark.fifth
def test_login_user(client):
    lg = client.post(
        "/api/v2/users/login", json={"email": 'abc@abc.com', "pwd": 'dklfjfkf373'}
    )
    assert lg.status_code == 200
    user = json.loads(lg.data)
    assert 'pwd' not in user

def update_user(client):
    pass

@pytest.mark.last
def test_delete_user(client):
    user = utils.login(client, "abc@abc.com", "dklfjfkf373")
    lg = client.delete(
        "/api/v2/users/{}".format(user['id']),
        headers=[("X-API-KEY", user["api_key"])],
    )
    assert lg.status_code == 200


# @pytest.mark.first
# def test_register(client):
#     lg = client.post(
#         "/api/v2/users/register", json={"email": t_con.TEST_USER, "pwd": t_con.TEST_PWD}
#     )
#     assert lg.status_code == 201 or lg.status_code == 409
