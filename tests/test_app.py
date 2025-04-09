# test_app.py

import pytest
from app import app, tracker

@pytest.fixture
def client():
    # Creates a test client using the Flask application configured for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route_exists(client):
    # Test that GET / returns HTTP 200 OK
    response = client.get('/')
    assert response.status_code == 200

def test_home_renders_skills(client):
    # Ensure skill names appear in the response content
    response = client.get('/')
    html = response.data.decode()
    for skill in tracker['skills']:
        assert skill in html

def test_home_renders_projects(client):
    # Ensure project titles appear in the response content
    response = client.get('/')
    html = response.data.decode()
    for project in tracker['projects']:
        assert project['title'] in html
