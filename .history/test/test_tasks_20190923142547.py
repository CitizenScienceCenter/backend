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

# def setup_module(module):
#     try:
#         db.bind('sqlite', ':memory:')
#     except TypeError:
#         pass
#     else:
#         db.generate_mapping(check_tables=False)

#     db.drop_all_tables(with_all_data=True)
#     db.create_tables()

@pytest.fixture(scope="module")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c

@pytest.fixture(scope="module")
def register(client):
    lg = client.post(
        f"{config.ROOT_URL}/users/register", json={"email": t_con.TEST_USER, "pwd": t_con.TEST_PWD}
    )
    assert lg.status_code == 201 or lg.status_code == 409

@pytest.fixture(scope="module")
def user(client, register):
    return utils.login(client, t_con.TEST_USER, t_con.TEST_PWD)

@pytest.fixture(scope="module")
def project(client, user):
    project_dict = {"name": "activity project", "description": "activity project"}
    return utils.create_project(client, project_dict, user["api_key"])


@pytest.fixture(scope="module")
def activity(client, user, project):
    act_dict = {
            "name": "Test Activity",
            "description": "Test Activity",
            "platform": "Both",
            "part_of": project['body']["id"],
        }
    print(act_dict)
    return client.post(
        f"{config.ROOT_URL}/activities",
        json=act_dict,
        headers=[("X-API-KEY", user["api_key"])]
    )

@pytest.fixture(scope="module")
def tasks(client, user, project, activity):
    pass

class TestActivities:
    @pytest.mark.run(order=12)
    def test_get_activities(self, client, user):
        lg = client.get(f"{config.ROOT_URL}/activities", headers=[("X-API-KEY", user["api_key"])])
        assert lg.status_code == 200

    @pytest.mark.run(order=13)
    def test_create_activity(self, client, user, project, activity):
        assert activity.status_code == 201

    @pytest.mark.run(order=14)
    def test_delete_activity(self, client, user, project, activity):
        act = json.loads(activity.data)
        lg = client.delete(f"{config.ROOT_URL}/activities/{act['body']['id']}", headers=[("X-API-KEY", user["api_key"])])
        assert lg.status_code == 200
    