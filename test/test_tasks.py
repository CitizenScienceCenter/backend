import pytest
import uuid
import configparser
import connexion
import json
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template, Response
from flask_cors import CORS

from app import Server

from test import t_con, utils, config

import prison

@pytest.fixture(scope="module")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c


@pytest.fixture(scope="module")
def register(client):
    lg = client.post(
        f"{config.ROOT_URL}/users/register",
        json={
            "username": t_con.TEST_USER,
            "email": t_con.TEST_USER,
            "pwd": t_con.TEST_PWD,
        },
    )
    assert lg.status_code == 201 or lg.status_code == 409


@pytest.fixture(scope="module")
def user(client, register):
    return utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)


@pytest.fixture(scope="module")
def project(client, user):
    project_dict = {"name": "project", "description": "project"}
    return utils.create_project(client, project_dict, user["api_key"])


@pytest.fixture(scope="module")
def tasks(client, user, project):
    pass


class TestProjects:
    @pytest.mark.run(order=12)
    def test_get_projects(self, client, user):
        lg = client.get(
            f"{config.ROOT_URL}/projects", headers=[("X-API-KEY", user["api_key"])]
        )
        assert lg.status_code == 200
        assert isinstance(json.loads(lg.data)['data'], list)
    
    @pytest.mark.run(order=13)
    def test_get_project(self, client, project, user):
        act = project
        lg = client.get(
            f"{config.ROOT_URL}/projects/{act['data']['id']}", headers=[("X-API-KEY", user["api_key"])]
        )        
        assert lg.status_code == 200
        assert json.loads(lg.data)['data']['id'] == act['data']['id']

    @pytest.mark.run(order=14)
    def test_delete_project(self, client, user, project):
        lg = client.delete(
            f"{config.ROOT_URL}/projects/{dict(project['data'])['id']}",
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert lg.status_code == 200
