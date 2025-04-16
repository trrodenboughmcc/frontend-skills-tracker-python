import requests

# Replace with your deployed frontend URL
FRONTEND_URL = "https://frontend-skills-tracker-python.onrender.com"

def test_homepage_renders_with_skills():
    response = requests.get(f"{FRONTEND_URL}/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert "Python" in response.text or "Flask" in response.text

def test_skill_levels_renders_with_data():
    response = requests.get(f"{FRONTEND_URL}/skill-levels")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert "skill" in response.text.lower()  # loosened assumption

def test_skill_levels_with_query_param():
    response = requests.get(f"{FRONTEND_URL}/skill-levels?skill=python")
    assert response.status_code == 200
    assert "python" in response.text.lower()
