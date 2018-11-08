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
    @pytest.mark.run(order=12)
    def test_get_projects(self, client, user):
        lg = client.get("/api/v1/projects", headers=[("X-API-KEY", user["api_key"])])
        assert lg.status_code == 200

    @pytest.mark.run(order=13)
    def test_create_project(self, client, user, group, project):
        assert project.status_code == 201

    @pytest.mark.run(order=14)
    def test_query_projects(self, client, user):
        q_statement = "(select:(fields:!(id,name,description),orderBy:(id:desc),tables:!(projects)))"
        lg = client.get(
            "/api/v1/projects?search_term={}".format(q_statement),
            headers=[("X-API-KEY", user["api_key"])],
        )
        proj = json.loads(lg.data)
        assert lg.status_code == 200
        assert len(proj) == 1
        assert 'description' in proj[0]
        assert proj[0]['description'] == 'Test Project'
        assert lg.status_code == 200

    @pytest.mark.run(order=15)
    def test_create_many_projects(self, client):
        pass

    @pytest.mark.run(order=16)
    def test_delete_all_projects_of_user(self, client):
        # TODO deletion of a project should either:
        # 1. remove the project, tasks AND ALL submissions
        # 2. Add a deleted flag to the info and hide it from get results (unless queried)
        pass

    @pytest.mark.run(order=17)
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
