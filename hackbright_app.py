import sqlite3
import traceback

DB = None
CONN = None

def delete_student(github):
    query = """DELETE FROM Students WHERE github = ?"""
    DB.execute(query, (github,))

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()

    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students VALUES (?, ?, ?) """
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    
    print "Sucessfully added student: %s %s"%(first_name, last_name)

def add_project(project_title, description, max_grade):
    query = """INSERT into Projects VALUES (?, ?, ?) """
    DB.execute(query, (project_title, description, max_grade))
    CONN.commit()
    
    print "Successfully added project: %s %s" %(project_title, description)

def get_project(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ? """
    DB.execute(query, (title,))
    row = DB.fetchone()
    
    return row
    
def project_grade(github, project_title):
    query = """SELECT grade FROM Grades JOIN Students 
                ON Students.github=Grades.student_github 
                WHERE project_title = ? and github = ?"""
    DB.execute(query, (project_title, github))
    row = DB.fetchone()
    
    return row

def give_grade(github, project_title, grade):
    query = """ INSERT into Grades VALUES (?, ?, ?) """
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    
    print "Grade %s added to %s for %s!" %(grade, project_title, github)

def show_grade(github):
    query = """SELECT project_title, grade FROM GRADES JOIN Students
                ON Students.github = Grades.student_github
                WHERE github = ?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    
    return rows

def show_all_grades(project_title):
    query = """SELECT * FROM GRADES WHERE project_title = ?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    
    return rows

def show_all_students():
    query = """SELECT * FROM Students"""
    DB.execute(query)
    rows= DB.fetchall()
    
    return rows

def show_all_projects():
    query = """SELECT * FROM Projects"""
    DB.execute(query)
    rows= DB.fetchall()
    
    return rows

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()
