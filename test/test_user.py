import pytest
import uuid
import configparser
import connexion
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template
from flask_cors import CORS

from db import orm_handler

from app import Server

from test import t_con, utils


@pytest.fixture(scope="module")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c


@pytest.mark.first
def test_register(client):
    lg = client.post(
        "/api/v2/users/register", json={"email": t_con.TEST_USER, "pwd": t_con.TEST_PWD}
    )
    assert lg.status_code == 201


@pytest.mark.second
def test_login(client):
    lg = client.post(
        "/api/v2/users/login", json={"email": t_con.TEST_USER, "pwd": t_con.TEST_PWD}
    )
    assert lg.status_code == 200


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
