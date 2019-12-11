import json
import pytest

from test import config

def login(client, username, password):
    u = client.post(f"{config.ROOT_URL}/users/login", json={
        "email": username,
        "pwd": password
    })
    assert u.status_code == 200
    u = json.loads(u.get_data())
    assert 'api_key' in u['data']
    return u['data']

def logout(client):
    return client.get(f"{config.ROOT_URL}/users/logout", follow_redirects=True)

def get_projects(client, api_key):
    g = client.get(f"{config.ROOT_URL}/projects", headers=[('X-API-KEY', api_key)])
    assert g.status_code == 200
    return json.loads(g.data)

def create_project(client, proj_dict, api_key):
    lg = client.post(
        f"{config.ROOT_URL}/projects",
        json=proj_dict,
        headers=[("X-API-KEY", api_key)],
    )
    assert lg.status_code == 201
    return json.loads(lg.data)

def delete_group(client, gid, api_key):
    lg = client.delete(
        f"{config.ROOT_URL}/project_groups/{0}".format(gid),
        headers=[("X-API-KEY", api_key)],
    )
    assert lg.status_code == 200
