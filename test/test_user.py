import json

import pytest

from app import Server
from test import t_con, utils
from datetime import datetime
import hashlib
import time

@pytest.fixture(scope="module")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c

@pytest.fixture(scope="module")
def anon_user(client):
    # now = str(time.time()).encode('utf-8')
    uid = '_anon {}'.format('dfjkshfuihvuiehfnijvrifbvrf') # TODO add extra details to avoid clash OR delegate to server?
    pwd = 'sbdshf783yfh4ub47iwhiu9heiu'
    u = {
        'username': uid,
        'pwd': pwd,
        'confirmed': False
    }
    return client.post(
        "/api/v2/users/register", json=u
    )


@pytest.mark.first
def test_register(client):
    lg = client.post(
        "/api/v2/users/register", json={"email": t_con.TEST_USER, "pwd": t_con.TEST_PWD}
    )
    assert lg.status_code == 201 or lg.status_code == 409


@pytest.mark.second
def test_login(client):
    lg = client.post(
        "/api/v2/users/login", json={"email": t_con.TEST_USER, "pwd": t_con.TEST_PWD}
    )
    assert lg.status_code == 200
    user = json.loads(lg.data)
    assert 'pwd' not in user

def test_convert_anonymous(client, anon_user):
    anon = json.loads(anon_user.data)
    lg = client.post(
        "/api/v2/users/register?from_anon={}".format(anon['id']), json={"email": 'abc@abc.com', "pwd": 'dklfjfkf373'}
    )
    assert lg.status_code == 201
    #TODO assert anon user does not exist
    #TODO assert new user exists
    #TODO assert user submissions match

@pytest.mark.run(order=3)
def test_login_fail(client):
    lg = client.post(
        "/api/v2/users/login",
        json={"email": "hfkjhdfgkj@gfhjkg.com", "pwd": "hdjkfhkjdhf"},
    )
    assert lg.status_code == 404

@pytest.mark.run(order=4)
def test_create_users(client):
    domain = "@test.com"
    for x in range(0,10):
        user = "user_{}".format(x)
        lg = client.post(
            "/api/v2/users/register", json={"email": "{}{}".format(user, domain), "pwd": user}
        )
        assert lg.status_code == 201

@pytest.mark.run(order=5)
def test_delete_users(client):
    domain = "@test.com"
    for x in range(0, 10):
        user = "user_{}".format(x)
        user = utils.login(client, "{}{}".format(user, domain), user)
        lg = client.delete(
            "/api/v2/users/{}".format(user['id']),
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert lg.status_code == 200

@pytest.mark.last
def test_delete_initial_user(client):
    user = utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)
    lg = client.delete(
        "/api/v2/users/{}".format(user['id']),
        headers=[("X-API-KEY", user["api_key"])],
    )
    assert lg.status_code == 200
