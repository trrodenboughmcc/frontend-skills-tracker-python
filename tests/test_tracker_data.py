from tracker_app.app import tracker

def test_tracker_has_required_keys():
    assert "skills" in tracker
    assert "projects" in tracker

def test_skills_is_list_of_strings():
    assert isinstance(tracker["skills"], list)
    for skill in tracker["skills"]:
        assert isinstance(skill, str)

def test_projects_is_list_of_dicts():
    assert isinstance(tracker["projects"], list)
    for project in tracker["projects"]:
        assert isinstance(project, dict)

def test_project_dicts_have_expected_keys():
    for project in tracker["projects"]:
        assert "title" in project
        assert "tech" in project
        assert "link" in project

def test_project_fields_are_all_strings():
    for project in tracker["projects"]:
        assert isinstance(project["title"], str)
        assert isinstance(project["tech"], str)
        assert isinstance(project["link"], str)
