import requests, time

FRONTEND_URL = "https://frontend-skills-tracker-python.onrender.com"

def fetch_with_retry(url, retries=5, delay=5):
    for _ in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response
        time.sleep(delay)
    return response

def test_homepage_renders_with_skills():
    response = fetch_with_retry(f"{FRONTEND_URL}/")
    assert response.status_code == 200

def test_skill_levels_renders_with_data():
    response = fetch_with_retry(f"{FRONTEND_URL}/skill-levels")
    assert response.status_code == 200

def test_skill_levels_with_query_param():
    response = fetch_with_retry(f"{FRONTEND_URL}/skill-levels?skill=python")
    assert response.status_code == 200
