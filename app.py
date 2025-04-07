from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory "database" of skills and projects
tracker = {
    "skills": ["Python", "Git", "HTML"],
    "projects": [
        {"title": "Personal Website", "tech": "HTML/CSS"},
        {"title": "Todo App", "tech": "Flask"}
    ]
}

@app.route('/')
def home():
    return render_template("index.html", tracker=tracker)

@app.route('/add-skill', methods=["POST"])
def add_skill():
    skill = request.form.get("skill").strip()
    if skill and skill not in tracker["skills"]:
        tracker["skills"].append(skill)
    return redirect(url_for('home'))

@app.route('/add-project', methods=["POST"])
def add_project():
    title = request.form.get("title").strip()
    tech = request.form.get("tech").strip()
    if title and tech:
        tracker["projects"].append({"title": title, "tech": tech})
    return redirect(url_for('home'))

@app.route('/remove-skill/<skill>')
def remove_skill(skill):
    tracker["skills"] = [s for s in tracker["skills"] if s.lower() != skill.lower()]
    return redirect(url_for('home'))

@app.route('/remove-project/<title>')
def remove_project(title):
    tracker["projects"] = [p for p in tracker["projects"] if p["title"].lower() != title.lower()]
    return redirect(url_for('home'))

@app.route('/debug')
def debug():
    return tracker

if __name__ == '__main__':
    app.run(debug=True)
