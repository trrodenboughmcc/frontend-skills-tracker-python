# test_tracker_data.py

from tracker_app.app import tracker

def test_tracker_has_skills_and_projects():
    assert 'skills' in tracker
    assert 'projects' in tracker
    assert isinstance(tracker['skills'], list)
    assert isinstance(tracker['projects'], list)

def test_skills_are_strings():
    for skill in tracker['skills']:
        assert isinstance(skill, str)

def test_projects_have_required_fields():
    for project in tracker['projects']:
        assert 'title' in project
        assert 'tech' in project
        assert 'link' in project
        assert isinstance(project['title'], str)
        assert isinstance(project['tech'], str)
        assert isinstance(project['link'], str)
