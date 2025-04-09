# ---------------------------
# Importing required modules
# ---------------------------

# pytest is the testing framework we're using
import pytest

# app and tracker are being imported from your main Flask app module
# 'app' is the Flask app instance
# 'tracker' is the dictionary holding your hardcoded skills and projects
from tracker_app.app import app, tracker

# html is a built-in Python module that helps decode HTML-escaped characters (like &amp; → &)
import html as html_lib


# ---------------------------
# Reusable client fixture for testing
# ---------------------------

@pytest.fixture
def client():
    """
    This fixture sets up a test version of the Flask app.
    It lets us simulate real HTTP requests to the app without starting a real server.
    """
    app.config['TESTING'] = True  # Enables test mode (e.g., better error messages)
    with app.test_client() as client:
        yield client  # Yielding lets tests use this preconfigured test client


# ===========================
# POSITIVE TESTS — expected behavior
# ===========================

def test_home_status_code(client):
    """
    Test that the homepage (GET /) returns a 200 OK response.
    This confirms the route is registered and renders successfully.
    """
    response = client.get('/')
    assert response.status_code == 200


def test_home_contains_skill_names(client):
    """
    Test that each skill in the tracker appears in the rendered HTML.
    This checks if the skill list is passed to the template and rendered.
    """
    response = client.get('/')
    html = response.data.decode()  # Convert the raw response bytes to a string
    for skill in tracker["skills"]:
        assert skill in html  # Each skill name should be somewhere in the HTML


def test_home_contains_project_titles(client):
    """
    Test that every project title is visible on the page.
    Ensures the template renders all project data correctly.
    """
    response = client.get('/')
    html = response.data.decode()
    for project in tracker["projects"]:
        assert project["title"] in html


# ===========================
# EDGE CASE TESTS — unusual but valid inputs
# ===========================

def test_empty_skills_list(monkeypatch, client):
    """
    Simulates the case where the skills list is empty.
    The fallback message 'No skills listed' should appear instead.
    """
    monkeypatch.setitem(tracker, "skills", [])  # Override the skills with an empty list
    response = client.get('/')
    assert "No skills listed" in response.data.decode()


def test_empty_projects_list(monkeypatch, client):
    """
    Simulates the case where no projects are defined.
    The fallback message 'No projects listed' should appear.
    """
    monkeypatch.setitem(tracker, "projects", [])
    response = client.get('/')
    assert "No projects listed" in response.data.decode()


def test_special_characters_in_skills(monkeypatch, client):
    """
    Tests if special characters in skills are rendered and displayed properly.
    Useful for ensuring HTML encoding doesn't break the output.
    """
    monkeypatch.setitem(tracker, "skills", ["C++", "Node.js", "React&Redux"])

    response = client.get('/')
    html = html_lib.unescape(response.data.decode())  # Decode any escaped characters

    # All special-character-based skill names should still show up as normal text
    assert "C++" in html and "Node.js" in html and "React&Redux" in html


def test_very_long_project_title(monkeypatch, client):
    """
    Tests how the app handles extremely long strings in project titles.
    Ensures no truncation, crash, or layout break occurs.
    """
    long_title = "A" * 500  # 500-character-long string
    monkeypatch.setitem(tracker, "projects", [{
        "title": long_title,
        "tech": "Python",
        "link": "https://example.com"
    }])

    response = client.get('/')
    assert long_title in response.data.decode()


# ===========================
# NEGATIVE TESTS — missing or malformed inputs
# ===========================

def test_project_missing_title(monkeypatch, client):
    """
    Simulates a project with no title field.
    The app should still return a valid page (not crash).
    """
    monkeypatch.setitem(tracker, "projects", [{
        "tech": "Python",
        "link": "https://example.com"
    }])
    response = client.get('/')
    assert response.status_code == 200


def test_project_missing_tech(monkeypatch, client):
    """
    Simulates a project missing the 'tech' field.
    Confirms the app still renders the page without errors.
    """
    monkeypatch.setitem(tracker, "projects", [{
        "title": "Incomplete Project",
        "link": "https://example.com"
    }])
    response = client.get('/')
    assert response.status_code == 200


def test_project_missing_link(monkeypatch, client):
    """
    Simulates a project missing the 'link' field.
    The app should still show the project title but omit the [View] link.
    """
    monkeypatch.setitem(tracker, "projects", [{
        "title": "No Link Project",
        "tech": "HTML"
    }])
    response = client.get('/')
    html = response.data.decode()

    # Project title should be visible
    assert "No Link Project" in html

    # Link element should not appear
    assert "[View]" not in html
