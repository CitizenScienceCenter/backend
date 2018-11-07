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
    group_dict = {"name": "project group", "description": "project group"}
    return utils.create_group(client, group_dict, user["api_key"])


@pytest.fixture(scope="module")
def project(client, user, group):
    return client.post(
        "/api/v1/projects",
        json={
            "name": "Test Projects",
            "description": "Test Project",
            "platform": "Both",
            "owned_by": group["id"],
        },
        headers=[("X-API-KEY", user["api_key"])],
    )


class TestProjects:
    @pytest.mark.run(order=8)
    def test_get_projects(self, client, user):
        lg = client.get("/api/v1/projects", headers=[("X-API-KEY", user["api_key"])])
        assert lg.status_code == 200

    @pytest.mark.run(order=9)
    def test_create_project(self, client, user, group, project):
        assert project.status_code == 201

    @pytest.mark.run(order=10)
    def test_delete_project(self, client, user, group, project):
        pd = client.delete(
            "/api/v1/projects/{}".format(json.loads(project.data)["id"]),
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert pd.status_code == 200
        gd = client.delete(
            "/api/v1/groups/{}".format(group["id"]),
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert gd.status_code == 200
