from flask import Flask, render_template, request
import os

app = Flask(__name__)

# ------------------------------------------------------------------------
# INSTRUCTIONS FOR STUDENTS:
# ------------------------------------------------------------------------
# To customize this app with your own experience:
# 1. Update the "skills" list below:
#    - Change the "name" to your actual skill
#    - Update the "experience" number to how many years you’ve worked with it
#
# 2. Update the "projects" list:
#    - Add new projects you’ve worked on
#    - Include the technologies used in the "tech" field
#    - Add a live link or GitHub link to the "link" field
# ------------------------------------------------------------------------

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

# Route for the homepage
@app.route('/')
def home():
    # Renders index.html and passes in the tracker data
    return render_template('index.html', tracker=tracker)

# Route for the skill summary/overview page
@app.route('/skill-levels')
def skill_levels():
    # Get selected skill from query string (e.g. /skill-levels?skill=Python)
    selected_skill = request.args.get('skill', '').strip().lower()

    usage_count = {}            # Count of how many projects each skill is used in
    matches = []                # List of (project, skill) pairs
    skill_project_map = {}      # Maps skill → list of matching projects
    highlighted_rows = {}       # Flags which row should be visually highlighted

    # Initialize data structures for each skill
    for skill_obj in tracker["skills"]:
        skill = skill_obj["name"]
        usage_count[skill] = 0
        skill_project_map[skill] = []
        highlighted_rows[skill] = skill.lower() == selected_skill  # Highlight if matched

    # Populate usage counts and project matches
    for project in tracker["projects"]:
        for skill_obj in tracker["skills"]:
            skill = skill_obj["name"]
            if skill.lower() in project["tech"].lower():
                matches.append((project["title"], skill))
                usage_count[skill] += 1
                skill_project_map[skill].append(project["title"])

    # Sort skills by usage frequency (most used first)
    sorted_skills = sorted(usage_count.items(), key=lambda x: x[1], reverse=True)

    # Map skill names to years of experience
    years_of_experience = {s["name"]: s["experience"] for s in tracker["skills"]}

    # Find the first project where a specific skill appears (for demonstration)
    first_python_project, tries = find_first_project_with("Python")

    # Render the skills summary page and pass all tracking data
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

# Utility function: find the first project that includes the given skill
def find_first_project_with(skill_name):
    index = 0
    attempts = 0
    while index < len(tracker["projects"]):
        attempts += 1
        if skill_name.lower() in tracker["projects"][index]["tech"].lower():
            return tracker["projects"][index]["title"], attempts
        index += 1
    return "Not found", attempts

# Launch the Flask server
if __name__ == '__main__':
    # On deployment (e.g. Render), use the port provided by the environment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
