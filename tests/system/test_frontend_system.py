import pytest
from tracker_app.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!doctype html" in response.data.lower()

def test_skill_levels_page_loads(client):
    response = client.get("/skill-levels")
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!doctype html" in response.data.lower()

def test_skill_levels_query_param_works(client):
    response = client.get("/skill-levels?skill=python")
    assert response.status_code == 200
    assert b"python" in response.data.lower()
