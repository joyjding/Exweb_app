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

    if row:
        print """
        Student: %s %s
        Github account: %s"""%(row[0], row[1], row[2])
    else:
        print "No such data"

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

    if row:
        print """
        Title: %s
        Description: %s
        Max Grade: %s""" % (row[0], row[1], row[2])
    else:
        print "No such data"

def project_grade(github, project_title):
    query = """SELECT grade FROM Grades JOIN Students 
                ON Students.github=Grades.student_github 
                WHERE project_title = ? and github = ?"""
    DB.execute(query, (project_title, github))
    row = DB.fetchone()
    
    if row:
        print "Grade: %s" % row[0]
    else:
        print "No such data"

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

    if rows:
        print "All grades for %s" %github
        for row in rows:
            print "%s: %s" %(row[0], row[1])
    else:
        print "No such data"

def text_args(args):
    new_args = []
    string = ''
    is_quote = False

    for arg in args:

        # Check for quotes
        if arg[0] == '"' and arg[-1] == '"':
            arg = arg[1:-1]
            new_args.append(arg)
            is_quote = False
            continue
        elif arg[0] == '"':
            arg = arg[1:]
            is_quote = True
        elif arg[-1] == '"' and len(arg) > 1:
            arg = arg[:-1]
            is_quote = False
            
        # Add string within quotes, otherwise append all other elements separately
        if is_quote == True:
            string += arg + " "
        else:
            if len(string) > 0:
                string += arg
            else:
                string = arg
            new_args.append(string)
            string = ''


    return new_args

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]
        args = text_args(args)
        try:

            if command == "student":
                get_student_by_github(*args) 
            elif command == "new_student":
                make_new_student(*args)
            elif command == "add_project":
                add_project(*args)
            elif command == "get_project":
                get_project(*args)
            elif command == "project_grade":
                project_grade(*args)
            elif command == "give_grade":
                give_grade(*args)
            elif command == "show_grade":
                show_grade(*args)
            elif command == "delete_student":
                delete_student(*args)

        except TypeError, e:
            print """
Whoah, something went wrong. Please type one of the following valid commands:

======== Add Commands ========
new_student [first name] [last name] [github]
add_project [title] [description] [max grade]
give_grade [github] [title] [grade]

======== Get Commands ========
student [github]
get_project [title]
project_grade [github] [title]
show_grade [github]

======== Delete Commands ========
delete_student [github]
            """
            # traceback.print_exc(e)


if __name__ == "__main__":
    main()
