from flask import Flask, render_template
import os

app = Flask(__name__)

# Tracker data with skills (name + years of experience) and projects
tracker = {
    "skills": [
        {"name": "Python", "experience": 3},
        {"name": "Flask", "experience": 2},
        {"name": "SQL", "experience": 2},
        {"name": "HTML", "experience": 4},
        {"name": "CSS", "experience": 4},
        {"name": "JavaScript", "experience": 3},
        {"name": "Git", "experience": 5},
        {"name": "API", "experience": 2}
    ],
    "projects": [
        {
            "title": "Portfolio Website",
            "tech": "HTML, CSS, JavaScript",
            "link": "https://yourportfolio.com"
        },
        {
            "title": "Todo App",
            "tech": "Python, Flask, SQL, HTML, CSS",
            "link": "https://github.com/yourusername/todo-app"
        },
        {
            "title": "Weather Dashboard",
            "tech": "Python, Flask, API, JavaScript, HTML, CSS",
            "link": "https://github.com/yourusername/weather-dashboard"
        },
        {
            "title": "Blog CMS",
            "tech": "Flask, SQL, HTML, CSS",
            "link": "https://github.com/yourusername/blog-cms"
        },
        {
            "title": "Git Practice Project",
            "tech": "Python, Git",
            "link": "https://github.com/yourusername/git-practice"
        },
        {
            "title": "API Data Visualizer",
            "tech": "Python, API, JavaScript",
            "link": "https://github.com/yourusername/api-visualizer"
        }
    ]
}

@app.route('/')
def home():
    return render_template('index.html', tracker=tracker)

@app.route('/skill-levels')
def skill_levels():
    usage_count = {}
    matches = []
    skill_project_map = {}

    # Initialize counters and mappings
    for skill_obj in tracker["skills"]:
        skill = skill_obj["name"]
        usage_count[skill] = 0
        skill_project_map[skill] = []

    # Match skills to projects
    for project in tracker["projects"]:
        for skill_obj in tracker["skills"]:
            skill = skill_obj["name"]
            if skill.lower() in project["tech"].lower():
                matches.append((project["title"], skill))
                usage_count[skill] += 1
                skill_project_map[skill].append(project["title"])

    # Sort by usage count (most-used skills first)
    sorted_skills = sorted(usage_count.items(), key=lambda x: x[1], reverse=True)

    # Map skill names to years of experience
    years_of_experience = {s["name"]: s["experience"] for s in tracker["skills"]}

    # Find first project with Python
    first_python_project, tries = find_first_project_with("Python")

    return render_template(
        'levels.html',
        tracker=tracker,
        usage_count=usage_count,
        sorted_skills=sorted_skills,
        matches=matches,
        skill_project_map=skill_project_map,
        years_of_experience=years_of_experience,
        first_python_project=first_python_project,
        tries=tries
    )

def find_first_project_with(skill_name):
    index = 0
    attempts = 0
    while index < len(tracker["projects"]):
        attempts += 1
        if skill_name.lower() in tracker["projects"][index]["tech"].lower():
            return tracker["projects"][index]["title"], attempts
        index += 1
    return "Not found", attempts

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
