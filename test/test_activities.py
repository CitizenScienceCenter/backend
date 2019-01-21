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

from app import Server

from test import t_con, utils

import prison


@pytest.fixture(scope="module")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c


@pytest.fixture(scope="module")
def user(client):
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
            "part_of": project["id"],
        }
    print(act_dict)
    return client.post(
        "/api/v2/activities",
        json=act_dict,
        headers=[("X-API-KEY", user["api_key"])]
    )


class TestActivities:
    @pytest.mark.run(order=12)
    def test_get_activities(self, client, user):
        lg = client.get("/api/v2/activities", headers=[("X-API-KEY", user["api_key"])])
        assert lg.status_code == 200

    @pytest.mark.run(order=13)
    def test_create_activity(self, client, user, project, activity):
        assert activity.status_code == 201

    @pytest.mark.run(order=14)
    def test_query_activities(self, client, user):
        q_statement = "(select:(fields:!(id,name,description),orderBy:(id:desc),tables:!(activities)))"
        lg = client.get(
            "/api/v2/activities?search_term={}".format(q_statement),
            headers=[("X-API-KEY", user["api_key"])],
        )
        act = json.loads(lg.data)
        assert lg.status_code == 200
        assert 'description' in act[0]
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
        pd = client.delete(
            "/api/v2/activities/{}".format(json.loads(activity.data)["id"])
        )
        assert pd.status_code == 401

    @pytest.mark.run(order=17)
    def test_delete_activity(self, client, user, project, activity):
        pd = client.delete(
            "/api/v2/activities/{}".format(json.loads(activity.data)["id"]),
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert pd.status_code == 200
        gd = client.delete(
            "/api/v2/projects/{}".format(project["id"]),
            headers=[("X-API-KEY", user["api_key"])],
        )
        assert gd.status_code == 200
