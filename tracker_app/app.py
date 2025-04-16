from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

# Your deployed backend base URL
BACKEND_API_URL = "https://skills-tracker-backend.onrender.com/api"

@app.route('/')
def home():
    skills = requests.get(f"{BACKEND_API_URL}/skills").json()
    projects = requests.get(f"{BACKEND_API_URL}/projects").json()
    tracker = {
        "skills": skills,
        "projects": projects
    }
    return render_template('index.html', tracker=tracker)

@app.route('/health')
def health():
    try:
        r = requests.get(f"{BACKEND_API_URL}/skills", timeout=5)
        return {"status": "ok", "code": r.status_code}, 200
    except Exception as e:
        return {"status": "backend unreachable", "error": str(e)}, 502

@app.route('/skill-levels')
def skill_levels():
    selected_skill = request.args.get('skill', '').strip().lower()

    skills = requests.get(f"{BACKEND_API_URL}/skills").json()
    projects = requests.get(f"{BACKEND_API_URL}/projects").json()
    usage_count = requests.get(f"{BACKEND_API_URL}/skill-usage").json()

    matches = []
    skill_project_map = {}
    highlighted_rows = {}

    for skill in skills:
        skill_name = skill["name"]
        highlighted_rows[skill_name] = skill_name.lower() == selected_skill
        skill_project_map[skill_name] = []
        for project in projects:
            if skill_name.lower() in project["tech"].lower():
                matches.append((project["title"], skill_name))
                skill_project_map[skill_name].append(project["title"])

    sorted_skills = sorted(usage_count.items(), key=lambda x: x[1], reverse=True)
    years_of_experience = {s["name"]: s["experience"] for s in skills}
    first_python_project, tries = find_first_project_with(projects, "Python")

    tracker = {
        "skills": skills,
        "projects": projects
    }

    return render_template(
        'levels.html',
        tracker=tracker,
        usage_count=usage_count,
        sorted_skills=sorted_skills,
        matches=matches,
        skill_project_map=skill_project_map,
        years_of_experience=years_of_experience,
        first_python_project=first_python_project,
        tries=tries,
        highlighted_rows=highlighted_rows,
        selected_skill=selected_skill
    )

def find_first_project_with(projects, skill_name):
    index = 0
    attempts = 0
    while index < len(projects):
        attempts += 1
        if skill_name.lower() in projects[index]["tech"].lower():
            return projects[index]["title"], attempts
        index += 1
    return "Not found", attempts

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
