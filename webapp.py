from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/add_student")
def add_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)
    return render_template("student_info.html", first_name=first_name, last_name=last_name, github=github)

@app.route("/add_project")
def add_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    desc = request.args.get("desc")
    max_grade = request.args.get("max_grade")
    hackbright_app.add_project(project_title, desc, max_grade)
    return render_template("main.html")

@app.route("/add_grade")
def add_grade():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    grade = request.args.get("grade")
    github = request.args.get("github")
    hackbright_app.give_grade(github, project_title, grade)
    return get_student(github)

@app.route("/get_student")
def get_student(student_github=None):
    hackbright_app.connect_to_db()
    if not student_github:
        student_github = request.args.get("github")

    profile = hackbright_app.get_student_by_github(student_github)
    grades = hackbright_app.show_grade(student_github)

    html = render_template("student_info.html", first_name=profile[0], last_name=profile[1], github=profile[2], grades=grades)
    return html

@app.route("/get_project")
def get_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    project = hackbright_app.get_project(project_title)

    return render_template("main.html", view_project=True, title=project[0], description=project[1], max_grade=project[2])
    
@app.route("/get_grades")
def get_grades():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    project_grades = hackbright_app.show_all_grades(project_title)
    html = render_template("project_grades.html", project_title=project_title, project_grades = project_grades)
    return html

@app.route("/all_students")
def all_students():
    hackbright_app.connect_to_db()
    names = hackbright_app.show_all_students()
    return render_template("main.html", all_students=True, students=names)

@app.route("/all_projects")
def all_projects():
    hackbright_app.connect_to_db()
    projects = hackbright_app.show_all_projects()
    return render_template("main.html", all_projects=True, projects=projects)

if __name__ == "__main__":
    app.run(debug=True)