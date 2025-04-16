import pytest
from unittest.mock import patch
from tracker_app.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

# Mock data used across multiple tests
mock_skills = [
    {"name": "Python", "experience": 3},
    {"name": "Flask", "experience": 2}
]

mock_projects = [
    {"title": "API Visualizer", "tech": "Python, API", "link": "#"},
    {"title": "Blog CMS", "tech": "Flask", "link": "#"}
]

mock_usage = {
    "Python": 1,
    "Flask": 1
}

# -----------------------------
# / route (homepage) tests
# -----------------------------

@patch("tracker_app.app.requests.get")
def test_home_page_renders_skills_and_projects(mock_get, client):
    mock_get.side_effect = [
        MockResponse(mock_skills),
        MockResponse(mock_projects)
    ]
    response = client.get("/")
    assert response.status_code == 200
    assert b"Python" in response.data
    assert b"API Visualizer" in response.data

# -----------------------------
# /skill-levels route tests
# -----------------------------

@patch("tracker_app.app.requests.get")
def test_skill_levels_renders_sorted_skills(mock_get, client):
    mock_get.side_effect = [
        MockResponse(mock_skills),
        MockResponse(mock_projects),
        MockResponse(mock_usage)
    ]
    response = client.get("/skill-levels")
    assert response.status_code == 200
    assert b"Python" in response.data
    assert b"Flask" in response.data

@patch("tracker_app.app.requests.get")
def test_skill_levels_highlight_selected_skill(mock_get, client):
    mock_get.side_effect = [
        MockResponse(mock_skills),
        MockResponse(mock_projects),
        MockResponse(mock_usage)
    ]
    response = client.get("/skill-levels?skill=flask")
    assert response.status_code == 200
    assert b"Flask" in response.data
