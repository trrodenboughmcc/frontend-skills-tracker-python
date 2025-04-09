import pytest
from tracker_app.app import app, tracker

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- POSITIVE TESTS ---

def test_home_status_code(client):
    """Home page should return status code 200."""
    response = client.get('/')
    assert response.status_code == 200

def test_home_contains_skill_names(client):
    """Each skill should be visible in the HTML output."""
    response = client.get('/')
    html = response.data.decode()
    for skill in tracker["skills"]:
        assert skill in html

def test_home_contains_project_titles(client):
    """Each project title should be visible in the HTML output."""
    response = client.get('/')
    html = response.data.decode()
    for project in tracker["projects"]:
        assert project["title"] in html

# --- EDGE CASE TESTS ---

def test_empty_skills_list(monkeypatch, client):
    """If skills list is empty, fallback message should show."""
    monkeypatch.setitem(tracker, "skills", [])
    response = client.get('/')
    assert "No skills listed" in response.data.decode()

def test_empty_projects_list(monkeypatch, client):
    """If projects list is empty, fallback message should show."""
    monkeypatch.setitem(tracker, "projects", [])
    response = client.get('/')
    assert "No projects listed" in response.data.decode()

def test_special_characters_in_skills(monkeypatch, client):
    """Skills with special characters should render safely."""
    monkeypatch.setitem(tracker, "skills", ["C++", "Node.js", "React&Redux"])
    response = client.get('/')
    html = response.data.decode()
    assert "C++" in html and "Node.js" in html and "React&Redux" in html

def test_very_long_project_title(monkeypatch, client):
    """Ensure the app can handle very long titles."""
    long_title = "A" * 500
    monkeypatch.setitem(tracker, "projects", [{
        "title": long_title,
        "tech": "Python",
        "link": "https://example.com"
    }])
    response = client.get('/')
    assert long_title in response.data.decode()

# --- NEGATIVE TESTS ---

def test_project_missing_title(monkeypatch, client):
    """Missing title should cause an error or skip rendering."""
    monkeypatch.setitem(tracker, "projects", [{
        "tech": "Python",
        "link": "https://example.com"
    }])
    response = client.get('/')
    assert response.status_code == 200  # Should not crash

def test_project_missing_tech(monkeypatch, client):
    """Missing tech should not break the page."""
    monkeypatch.setitem(tracker, "projects", [{
        "title": "Incomplete Project",
        "link": "https://example.com"
    }])
    response = client.get('/')
    assert response.status_code == 200

def test_project_missing_link(monkeypatch, client):
    """Missing link should render without the 'View' button."""
    monkeypatch.setitem(tracker, "projects", [{
        "title": "No Link Project",
        "tech": "HTML"
    }])
    response = client.get('/')
    html = response.data.decode()
    assert "No Link Project" in html
    assert "[View]" not in html
