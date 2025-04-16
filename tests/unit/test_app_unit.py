import pytest
from tracker_app.app import app, find_first_project_with
from unittest.mock import patch

# -------------------------------
# Unit test: find_first_project_with
# -------------------------------

def test_find_first_project_with_found():
    mock_projects = [
        {"title": "Site Builder", "tech": "HTML"},
        {"title": "Data Tool", "tech": "Python"},
        {"title": "Chart App", "tech": "D3.js"},
    ]
    result, tries = find_first_project_with(mock_projects, "Python")
    assert result == "Data Tool"
    assert tries == 2

def test_find_first_project_with_not_found():
    mock_projects = [
        {"title": "Site Builder", "tech": "HTML"},
        {"title": "Chart App", "tech": "JavaScript"},
    ]
    result, tries = find_first_project_with(mock_projects, "Python")
    assert result == "Not found"
    assert tries == len(mock_projects)

# -------------------------------
# Unit test: / route with mocked requests
# -------------------------------

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

@patch("tracker_app.app.requests.get")
def test_home_route_returns_html(mock_get, client):
    # Simulate two .get() calls: /skills and /projects
    mock_get.side_effect = [
        MockResponse([{"name": "Python", "experience": 3}]),
        MockResponse([{"title": "Todo App", "tech": "Python", "link": "#"}])
    ]
    response = client.get("/")
    assert response.status_code == 200
    assert b"Python" in response.data

@patch("tracker_app.app.requests.get")
def test_skill_levels_returns_html(mock_get, client):
    # Simulate three .get() calls: /skills, /projects, /skill-usage
    mock_get.side_effect = [
        MockResponse([{"name": "Python", "experience": 3}]),
        MockResponse([{"title": "Todo App", "tech": "Python", "link": "#"}]),
        MockResponse({"Python": 1})
    ]
    response = client.get("/skill-levels")
    assert response.status_code == 200
    assert b"Python" in response.data

# -------------------------------
# Mock Response class
# -------------------------------

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json
