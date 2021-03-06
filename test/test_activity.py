import pytest
import uuid
import configparser
import connexion
import json
from connexion import NoContent
from connexion.resolver import RestyResolver

from flask import session, request, g, render_template, Response
from flask_cors import CORS

from db import models

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
    project_dict = {"name": "activity project", "description": "activity project"}
    return utils.create_project(client, project_dict, user["api_key"])


@pytest.fixture(scope="module")
def activity(client, user, project):
    act_dict = {
        "name": "Test Activity",
        "description": "Test Activity",
        "platform": "Both",
        "part_of": project["data"]["id"],
    }
    return client.post(
        f"{config.ROOT_URL}/activities",
        json=act_dict,
        headers=[("X-API-KEY", user["api_key"])],
    )


class TestActivities:
    @pytest.mark.run(order=12)
    def test_get_activities(self, client, user):
        lg = client.get(
            f"{config.ROOT_URL}/activities", headers=[("X-API-KEY", user["api_key"])]
        )
        assert lg.status_code == 200

    @pytest.mark.run(order=13)
    def test_create_activity(self, client, user, project, activity):
        assert activity.status_code == 201

    @pytest.mark.run(order=14)
    def test_query_activities(self, client, user):
        q_statement = "(select:(fields:!(id,name,description),orderBy:(id:desc),tables:!(activities)))"
        lg = client.get(
            f"{config.ROOT_URL}/activities?search_term={q_statement}",
            headers=[("X-API-KEY", user["api_key"])],
        )
        act = json.loads(lg.data)
        assert lg.status_code == 200
        assert "description" in act["data"][0]
        assert lg.status_code == 200

    @pytest.mark.run(order=15)
    def test_create_many_projects(self, client):
        pass

    @pytest.mark.run(order=16)
    def test_delete_all_projects_of_user(self, client):
        # TODO deletion of a project should either:
        # 1. remove the project, tasks AND ALL submissions
        # 2. Add a deleted flag/make it inactive to the info and hide it from get results (unless queried)
        pass

    @pytest.mark.run(order=18)
    def test_delete_activity(self, client, user, project, activity):
        act = json.loads(activity.data)
        print(act)
        pd = client.delete(f"{config.ROOT_URL}/activities/{act['data']['id']}")
        assert pd.status_code == 401

    @pytest.mark.run(order=17)
    def test_delete_activity_and_project(self, client, user, project, activity):
        act = json.loads(activity.data)
        pd = client.delete(
            f"{config.ROOT_URL}/activities/{act['data']['id']}",
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert pd.status_code == 200
        gd = client.delete(
            f"{config.ROOT_URL}/projects/{project['data']['id']}",
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert gd.status_code == 200
