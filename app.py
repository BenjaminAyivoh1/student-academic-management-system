from db import get_connection
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():

    connection = get_connection()

    total_students = connection.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    average_gpa = connection.execute(
        "SELECT AVG(gpa) FROM students"
    ).fetchone()[0]

    highest_gpa = connection.execute(
        "SELECT MAX(gpa) FROM students"
    ).fetchone()[0]

    connection.close()

    if average_gpa is None:
        average_gpa = 0

    if highest_gpa is None:
        highest_gpa = 0

    return render_template(
        "index.html",
        total_students=total_students,
        average_gpa=round(average_gpa, 2),
        highest_gpa=highest_gpa
    )

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        programme = request.form["programme"]
        level = request.form["level"]
        gpa = request.form["gpa"]

        connection = get_connection()

        cursor = connection.cursor()

        # Generate Student ID
        cursor.execute(
            "SELECT MAX(id) FROM students"
        )

        last_id = cursor.fetchone()[0]

        if last_id is None:
            last_id = 0

        student_id = f"UG{last_id + 1:03}"

        cursor.execute(
            """
            INSERT INTO students
            (student_id, name, age, programme, level, gpa)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                name,
                age,
                programme,
                level,
                gpa
            )
        )

        connection.commit()
        connection.close()

        return redirect("/view_students")

    return render_template("add_student.html")

@app.route("/view_students")
def view_students():

    connection = get_connection()

    students = connection.execute(
        "SELECT * FROM students"
    ).fetchall()
    

    connection.close()

    return render_template(
        "view_students.html",
        students=students
    )

@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()

    connection.close()

    return redirect("/view_students")

@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    connection = get_connection()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        programme = request.form["programme"]
        level = request.form["level"]
        gpa = request.form["gpa"]

        connection.execute(
            """
            UPDATE students
            SET name = ?,
                age = ?,
                programme = ?,
                level = ?,
                gpa = ?
            WHERE id = ?
            """,
            (
            name,
            age,
            programme,
            level,
            gpa,
            student_id
            )
        )

        connection.commit()
        connection.close()

        return redirect("/view_students")

    student = connection.execute(
        """
        SELECT *
        FROM students
        WHERE id = ?
        """,
        (student_id,)
    ).fetchone()

    connection.close()

    return render_template(
        "edit_student.html",
        student=student
    )

@app.route("/search_student", methods=["GET", "POST"])
def search_student():

    results = []

    if request.method == "POST":

        search_name = request.form["search"]

        connection = get_connection()

        results = connection.execute(
            """
            SELECT *
            FROM students
            WHERE name LIKE ?
            """,
            (f"%{search_name}%",)
        ).fetchall()

        connection.close()

    return render_template(
        "search_student.html",
        results=results
    )

@app.route("/about")
def about():
    return render_template("about.html")
if __name__ == "__main__":
    app.run(debug=True)