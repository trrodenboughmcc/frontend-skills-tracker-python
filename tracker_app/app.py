from flask import Flask, render_template
import os

app = Flask(__name__)

tracker = {
    "skills": [
        "Python",
        "Flask",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "API"
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

@app.route('/skill-levels')
def skill_levels():
    # Map realistic years of experience to each skill
    years_of_experience = {
        "Python": 3,
        "Flask": 2,
        "SQL": 2,
        "HTML": 4,
        "CSS": 4,
        "JavaScript": 3,
        "Git": 5,
        "API": 2
    }

    usage_count = {}
    matches = []
    skill_project_map = {skill: [] for skill in tracker["skills"]}

    for skill in tracker["skills"]:
        usage_count[skill] = 0

    for project in tracker["projects"]:
        for skill in tracker["skills"]:
            if skill.lower() in project["tech"].lower():
                matches.append((project["title"], skill))
                usage_count[skill] += 1
                skill_project_map[skill].append(project["title"])

    sorted_skills = sorted(usage_count.items(), key=lambda x: x[1], reverse=True)

    first_python_project, tries = find_first_project_with("Python")

    return render_template(
        'levels.html',
        years_of_experience=years_of_experience,
        usage_count=usage_count,
        sorted_skills=sorted_skills,
        matches=matches,
        skill_project_map=skill_project_map,
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
