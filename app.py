from flask import Flask, request, render_template, redirect, url_for
from database import get_database, close_database

app = Flask(__name__)
app.teardown_appcontext(close_database)

# Function to execute queries
def execute_query(query, params=()):
    connection = get_database()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()


# Route to render the homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")

# Function to create a new teacher
@app.route("/create-teacher", methods=["GET", "POST"])
def create_teacher():
    if request.method == "POST":
        data = request.form
        query = """
        INSERT INTO teachers (name, extra_role, job_role, department_id, working_hours, employee_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        execute_query(query, (data["name"], data["extra_role"], data["job_role"], data["department_id"], data["working_hours"], data["employee_id"]))
        return redirect(url_for("view_teachers"))
    return render_template("create_teacher.html")

# Function to edit a teacher
@app.route("/edit-teacher/<int:teacher_id>", methods=["POST"])
def edit_teacher(teacher_id):
    if request.method == "POST":
        data = request.form
        query = """
        UPDATE teachers 
        SET name = ?, extra_role = ?, job_role = ?, department_id = ?, working_hours = ?, employee_id = ?
        WHERE id = ?
        """
        execute_query(query, (data["name"], data["extra_role"], data["job_role"], data["department_id"], data["working_hours"], data["employee_id"], teacher_id))
        return redirect(url_for("view_teachers"))

# Function to delete a teacher
@app.route("/delete-teacher/<int:teacher_id>", methods=["POST"])
def delete_teacher(teacher_id):
    if request.method == "POST":
        query = "DELETE FROM teachers WHERE id = ?"
        execute_query(query, (teacher_id,))
        return redirect(url_for("view_teachers"))

# Function to create a new course
@app.route("/create-course", methods=["GET", "POST"])
def create_course():
    if request.method == "POST":
        data = request.form
        query = """
        INSERT INTO courses (name, credits, classes_per_week, teacher_id)
        VALUES (?, ?, ?, ?)
        """
        execute_query(query, (data["name"], data["credits"], data["classes_per_week"], data["teacher_id"]))
        return redirect(url_for("view_courses"))
    return render_template("create_course.html")

# Function to edit a course
@app.route("/edit-course/<int:course_id>", methods=["POST"])
def edit_course(course_id):
    if request.method == "POST":
        data = request.form
        query = """
        UPDATE courses 
        SET name = ?, credits = ?, classes_per_week = ?, teacher_id = ?
        WHERE id = ?
        """
        execute_query(query, (data["name"], data["credits"], data["classes_per_week"], data["teacher_id"], course_id))
        return redirect(url_for("view_courses"))

# Function to delete a course
@app.route("/delete-course/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    if request.method == "POST":
        query = "DELETE FROM courses WHERE id = ?"
        execute_query(query, (course_id,))
        return redirect(url_for("view_courses"))

# Function to create a new classroom
@app.route("/create-classroom", methods=["GET", "POST"])
def create_classroom():
    if request.method == "POST":
        data = request.form
        query = """
        INSERT INTO classrooms (number, capacity)
        VALUES (?, ?)
        """
        execute_query(query, (data["number"], data["capacity"]))
        return redirect(url_for("view_classrooms"))
    return render_template("create_classroom.html")

# Function to edit a classroom
@app.route("/edit-classroom/<int:classroom_id>", methods=["POST"])
def edit_classroom(classroom_id):
    if request.method == "POST":
        data = request.form
        query = """
        UPDATE classrooms 
        SET number = ?, capacity = ?
        WHERE id = ?
        """
        execute_query(query, (data["number"], data["capacity"], classroom_id))
        return redirect(url_for("view_classrooms"))

# Function to delete a classroom
@app.route("/delete-classroom/<int:classroom_id>", methods=["POST"])
def delete_classroom(classroom_id):
    if request.method == "POST":
        query = "DELETE FROM classrooms WHERE id = ?"
        execute_query(query, (classroom_id,))
        return redirect(url_for("view_classrooms"))

# Function to view all classrooms
@app.route("/classrooms", methods=["GET"])
def view_classrooms():
    query = "SELECT * FROM classrooms"
    connection = get_database()
    cursor = connection.cursor()
    cursor.execute(query)
    classrooms = cursor.fetchall()
    return render_template("view_classrooms.html", classrooms=classrooms)

# Function to view all teachers
@app.route("/teachers", methods=["GET"])
def view_teachers():
    query = "SELECT * FROM teachers"
    connection = get_database()
    cursor = connection.cursor()
    cursor.execute(query)
    teachers = cursor.fetchall()
    return render_template("view_teachers.html", teachers=teachers)

# Function to view all courses
@app.route("/courses", methods=["GET"])
def view_courses():
    query = "SELECT * FROM courses"
    connection = get_database()
    cursor = connection.cursor()
    cursor.execute(query)
    courses = cursor.fetchall()
    return render_template("view_courses.html", courses=courses)

@app.route("/timetable", methods=["GET", "POST"])
def view_timetable():
    connection = get_database()
    cursor = connection.cursor()

    # Fetch teachers and courses for dropdowns
    cursor.execute("SELECT id, name FROM teachers")
    teachers = cursor.fetchall()
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()

    if request.method == "POST":
        teacher_id = request.form.get("teacher_id")
        if teacher_id:
            # Fetch timetable for a specific teacher
            query = """
            SELECT tt.id, t.name AS teacher_name, c.name AS course_name, cl.number AS classroom_number,
                   tt.day_of_week, tt.start_time, tt.end_time
            FROM timetable tt
            INNER JOIN teachers t ON tt.teacher_id = t.id
            INNER JOIN courses c ON tt.course_id = c.id
            INNER JOIN classrooms cl ON tt.classroom_id = cl.id
            WHERE tt.teacher_id = ?
            """
            cursor.execute(query, (teacher_id,))
        else:
            # Fetch timetable for all teachers
            query = """
            SELECT tt.id, t.name AS teacher_name, c.name AS course_name, cl.number AS classroom_number,
                   tt.day_of_week, tt.start_time, tt.end_time
            FROM timetable tt
            INNER JOIN teachers t ON tt.teacher_id = t.id
            INNER JOIN courses c ON tt.course_id = c.id
            INNER JOIN classrooms cl ON tt.classroom_id = cl.id
            """
            cursor.execute(query)

        timetable = cursor.fetchall()
        return render_template("view_timetable.html", teachers=teachers, courses=courses, timetable=timetable)

    # Default to showing timetable for all teachers
    cursor.execute("""
    SELECT tt.id, t.name AS teacher_name, c.name AS course_name, cl.number AS classroom_number,
           tt.day_of_week, tt.start_time, tt.end_time
    FROM timetable tt
    INNER JOIN teachers t ON tt.teacher_id = t.id
    INNER JOIN courses c ON tt.course_id = c.id
    INNER JOIN classrooms cl ON tt.classroom_id = cl.id
    """)
    timetable = cursor.fetchall()
    return render_template("view_timetable.html", teachers=teachers, courses=courses, timetable=timetable)

@app.route("/generate-timetable", methods=["GET", "POST"])
def generate_timetable():
    if request.method == "POST":
        connection = get_database()
        cursor = connection.cursor()

        # Fetch teachers, courses, and classrooms
        teacher_query = "SELECT id FROM teachers"
        course_query = "SELECT id, classes_per_week FROM courses"
        classroom_query = "SELECT id FROM classrooms"

        cursor.execute(teacher_query)
        teachers = [row[0] for row in cursor.fetchall()]
        cursor.execute(course_query)
        courses = cursor.fetchall()
        cursor.execute(classroom_query)
        classrooms = [row[0] for row in cursor.fetchall()]

        if not teachers or not courses or not classrooms:
            return "Ensure teachers, courses, and classrooms are present in the database.", 400

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        start_hour = 9
        end_hour = 17
        time_slot_duration = 1
        gap_duration = 1

        timetable = []
        teacher_schedule = {teacher_id: {day: [] for day in days} for teacher_id in teachers}
        course_assignments = {course_id: teachers[i % len(teachers)] for i, (course_id, _) in enumerate(courses)}

        for day in days:
            for hour in range(start_hour, end_hour, time_slot_duration + gap_duration):
                for classroom_id in classrooms:
                    for course_id, teacher_id in course_assignments.items():
                        if hour not in teacher_schedule[teacher_id][day]:
                            timetable.append((teacher_id, course_id, classroom_id, day, f"{hour}:00", f"{hour + time_slot_duration}:00"))
                            teacher_schedule[teacher_id][day].extend(range(hour, hour + time_slot_duration + gap_duration))
                            break

        insert_query = """
        INSERT INTO timetable (teacher_id, course_id, classroom_id, day_of_week, start_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(insert_query, timetable)
        connection.commit()

        return redirect(url_for("view_timetable"))

    return render_template("generate_timetable.html")

if __name__ == "__main__":
    app.run(debug=True)
