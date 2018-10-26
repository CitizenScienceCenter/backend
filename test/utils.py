import json
import pytest

def login(client, username, password):
    u = client.post('/api/v1/users/login', json={
        "email": username,
        "pwd": password
    }, follow_redirects=True)
    assert u.status_code == 200
    u = json.loads(u.get_data())
    assert 'api_key' in u
    return u


def logout(client):
    return client.get('/api/v1/users/logout', follow_redirects=True)

def get_groups(client, api_key):
    g = client.get('/api/v1/groups', headers=[('X-API-KEY', api_key)])
    assert g.status_code == 200
    return json.loads(g.get_data())