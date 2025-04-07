# Import Flask framework and render_template to display HTML templates
from flask import Flask, render_template

# Create an instance of the Flask app
app = Flask(__name__)

# -----------------------------
# Hardcoded Data for the App
# -----------------------------

# The 'tracker' dictionary contains two main parts:
# 1. A list of skills
# 2. A list of projects, each with title, technologies used, and a link
tracker = {
    # List of skills you might know or want to showcase
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

    # List of projects — this is where you can add/edit your own work
    "projects": [
        {
            "title": "Portfolio Website",  # Name of the project
            "tech": "HTML, CSS, JavaScript",  # Comma-separated tech stack
            "link": "https://yourportfolio.com"  # Link to live site or repo
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

# -----------------------------
# Flask Route to Render the Page
# -----------------------------

@app.route('/')
def home():
    # Pass the 'tracker' dictionary into the HTML template
    return render_template('index.html', tracker=tracker)

# -----------------------------
# Run the Flask App
# -----------------------------
if __name__ == '__main__':
    # Run in debug mode to auto-reload when changes are made
    app.run(debug=True)
