import json
from test import t_con, utils, config
import pytest

from app import Server

@pytest.fixture(scope="session")
def client():
    s = Server()
    with s.connexion_app.app.test_client() as c:
        yield c

@pytest.fixture(scope="session")
def create_anon_user(client):
    pass

def login_anon_user(client, create_anon_user):
    pass



