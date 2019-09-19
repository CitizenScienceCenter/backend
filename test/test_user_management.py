import json

import pytest

from app import Server
from test import t_con, utils, config
from datetime import datetime
import hashlib
import time


anon_name = '_anon{}'.format('dfjkshfuihvuiehfnijvrifbvrf')
anon_pwd = 'sbdshf783yfh4ub47iwhiu9heiu' 

@pytest.fixture(scope="session")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c

@pytest.fixture(scope="session")
def anonymous_user(client):
    u = {
        'username': anon_name,
        'pwd': anon_pwd,
        'confirmed': False,
        'info': {
            'anonymous': True
        }
    }
    reg = client.post(
        f"{config.ROOT_URL}/users/register", json=u
    )
    print(reg.data)
    assert reg.status_code == 201 or reg.status_code == 409


@pytest.fixture(scope="session")
def login_anonymous(client, anonymous_user):
    lg = client.post(
        f"{config.ROOT_URL}/users/login", json={"username": anon_name, "pwd": anon_pwd}
    )
    assert lg.status_code == 200
    user = json.loads(lg.data)
    assert 'pwd' not in user
    lg = client.post(
        f"{config.ROOT_URL}/users/register", json={"email": 'abc@abc.com', "pwd": 'dklfjfkf373'},
        headers=[("X-Api-Key", user['api_key'])],
    )
    assert lg.status_code == 201
    return user

@pytest.mark.first
def test_convert_anonymous_user(client, login_anonymous):
    assert True


@pytest.mark.second
def test_anonymous_fail(client):
    lg = client.post(
        f"{config.ROOT_URL}/users/login", json={"username": anon_name, "pwd": anon_pwd}
    )
    assert lg.status_code == 404

@pytest.mark.third
def test_login_user(client):
    lg = client.post(
        f"{config.ROOT_URL}/users/login", json={"email": 'abc@abc.com', "pwd": 'dklfjfkf373'}
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
        f"{config.ROOT_URL}/users/{user['id']}",
        headers=[("X-API-KEY", user["api_key"])],
    )
    assert lg.status_code == 200


# @pytest.mark.first
# def test_register(client):
#     lg = client.post(
#         "/api/v2/users/register", json={"email": t_con.TEST_USER, "pwd": t_con.TEST_PWD}
#     )
#     assert lg.status_code == 201 or lg.status_code == 409
