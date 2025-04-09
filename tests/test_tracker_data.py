# Import the 'tracker' dictionary from the Flask app module
# This holds all the hardcoded skills and projects for the app
from tracker_app.app import tracker

# ---------------------------
# STRUCTURE & TYPE TESTS FOR THE TRACKER DICTIONARY
# ---------------------------

def test_tracker_has_required_keys():
    """
    Ensure the tracker dictionary contains both 'skills' and 'projects' keys.
    These are the top-level structures the app depends on.
    """
    assert "skills" in tracker
    assert "projects" in tracker


def test_skills_is_list_of_strings():
    """
    Validate that the 'skills' key holds a list,
    and that each item in that list is a string (e.g., "Python", "HTML").
    """
    assert isinstance(tracker["skills"], list)  # First, check the container is a list
    for skill in tracker["skills"]:
        assert isinstance(skill, str)  # Each individual skill must be a string


def test_projects_is_list_of_dicts():
    """
    Check that 'projects' is a list, and each item inside it is a dictionary.
    Each dictionary should represent one project.
    """
    assert isinstance(tracker["projects"], list)
    for project in tracker["projects"]:
        assert isinstance(project, dict)  # Each project should be a dictionary


# ---------------------------
# VALIDATION OF PROJECT FIELD STRUCTURE
# ---------------------------

def test_project_dicts_have_expected_keys():
    """
    Each project dictionary must include the expected keys:
    - 'title': name of the project
    - 'tech': comma-separated string of technologies used
    - 'link': URL to view the project
    """
    for project in tracker["projects"]:
        assert "title" in project
        assert "tech" in project
        assert "link" in project


def test_project_fields_are_all_strings():
    """
    All values inside each project dictionary should be strings.
    This ensures consistent rendering and avoids runtime errors in templates.
    """
    for project in tracker["projects"]:
        assert isinstance(project["title"], str)
        assert isinstance(project["tech"], str)
        assert isinstance(project["link"], str)
