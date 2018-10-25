def login(client, username, password):
    return client.post('/api/v1/users/login', json={
        "email": username,
        "pwd": password
    }, follow_redirects=True)


def logout(client):
    return client.get('/api/v1/users/logout', follow_redirects=True)