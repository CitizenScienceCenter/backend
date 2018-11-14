import json
import pytest

def login(client, username, password):
    u = client.post('/api/v2/users/login', json={
        "email": username,
        "pwd": password
    }, follow_redirects=True)
    assert u.status_code == 200
    u = json.loads(u.get_data())
    assert 'api_key' in u
    return u


def logout(client):
    return client.get('/api/v2/users/logout', follow_redirects=True)

def get_projects(client, api_key):
    g = client.get('/api/v2/projects', headers=[('X-API-KEY', api_key)])
    assert g.status_code == 200
    return json.loads(g.data)

def create_project(client, proj_dict, api_key):
    lg = client.post(
        "/api/v2/projects",
        json=proj_dict,
        headers=[("X-API-KEY", api_key)],
    )
    assert lg.status_code == 201
    return json.loads(lg.data)

def delete_group(client, gid, api_key):
    lg = client.delete(
        "/api/v2/groups/{0}".format(gid),
        headers=[("X-API-KEY", api_key)],
    )
    assert lg.status_code == 200
