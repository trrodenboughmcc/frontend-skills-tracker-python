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

@app.route('/')
def home():
    return render_template('index.html', tracker=tracker)

@app.route('/skill-levels')
def skill_levels():
    # Generate levels using range()
    skill_levels = {}
    for i in range(len(tracker["skills"])):
        skill = tracker["skills"][i]
        skill_levels[skill] = f"Level {i + 1}"

    # Match skills to projects (nested loop)
    matches = []
    for project in tracker["projects"]:
        for skill in tracker["skills"]:
            if skill.lower() in project["tech"].lower():
                matches.append((project["title"], skill))

    # First project using 'Python' (while + break)
    first_python_project, tries = find_first_project_with("Python")

    return render_template('levels.html', skill_levels=skill_levels, matches=matches,
                           first_python_project=first_python_project, tries=tries)

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
