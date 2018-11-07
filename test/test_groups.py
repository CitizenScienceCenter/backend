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

import prison


@pytest.fixture(scope="module")
def client():
    with app.app.test_client() as c:
        yield c

@pytest.fixture(scope="module")
def user(client):
    return utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)

@pytest.fixture(scope="module")
def group(client, user):
    group_dict = {"name": "Test Group", "description": "A Test Group"}
    group = utils.create_group(client, group_dict, user["api_key"])
    return group

class TestGroups():

    def test_create_group(self, client, user, group):
        assert 'id' in group
        assert group['id'] is not None

    def test_query_groups(self, client, user):
        q_statement = "(select:(fields:!(id,name),orderBy:(id:desc),tables:!(groups)))"
        lg = client.get(
            "/api/v1/groups?search_term={}".format(q_statement),
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert lg.status_code == 200

    def test_delete_group(self, client, user, group):
        utils.delete_group(client, group["id"], user["api_key"])

    def test_create_groups__invalid(self, client, user):
        lg = client.post(
            "/api/v1/groups", json={}, headers=[("X-API-KEY", user["api_key"])]
        )
        assert lg.status_code == 400


