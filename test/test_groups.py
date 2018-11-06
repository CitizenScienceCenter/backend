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

@pytest.fixture(scope="function")
def user(client):
    return utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)


class TestGroups():


    @pytest.mark.run(order=4)
    def test_create_and_delete_groups(self, client, user):
        group_dict = {"name": "Test Group", "description": "A Test Group"}
        group = utils.create_group(client, group_dict, user["api_key"])
        utils.delete_group(client, group["id"], user["api_key"])

    @pytest.mark.run(order=5)
    def test_create_groups__invalid(self, client, user):
        lg = client.post(
            "/api/v1/groups", json={}, headers=[("X-API-KEY", user["api_key"])]
        )
        assert lg.status_code == 400

    @pytest.mark.run(order=6)
    def test_query_groups(self, client, user):
        q_statement = "(select:(fields:!(email,id,password),orderBy:(email:ASC,id:desc),tables:!(groups)))"
        lg = client.get(
            "/api/v1/groups?search_term={}".format(q_statement),
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert lg.status_code == 200

