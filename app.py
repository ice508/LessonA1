import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_school_key" 
DB_NAME = "school.db"

def init_db():
    """Initializes the database using our schema configuration script."""
    with sqlite3.connect(DB_NAME) as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())

@app.route("/")
def index():
    """GET Route: Fetches students, optionally filtering by search queries."""
    search_query = request.args.get("search", "").strip()
    
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if search_query:
            # Look for an exact match or use LIKE for partial ID matching
            cursor.execute(
                "SELECT student_id, name, age FROM students WHERE student_id LIKE ? ORDER BY name ASC",
                (f"%{search_query}%",)
            )
        else:
            cursor.execute("SELECT student_id, name, age FROM students ORDER BY name ASC")
            
        students = cursor.fetchall()
        
    return render_template("home.html", students=students, search_query=search_query)

@app.route("/add_student", methods=["POST"])
def add_student():
    """POST Route: Adds a new student to the roster."""
    student_id = request.form.get("student_id").strip()
    name = request.form.get("name").strip()
    age = request.form.get("age")

    if student_id and name and age:
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (student_id, name, age) VALUES (?, ?, ?)",
                    (student_id, name, int(age))
                )
                conn.commit()
                flash(f"Success: {name} has been registered!", "success")
        except sqlite3.IntegrityError:
            flash(f"Error: A student with ID '{student_id}' already exists!", "error")

    return redirect(url_for("index"))

@app.route("/delete_student/<string:student_id>", methods=["POST"])
def delete_student(student_id):
    """POST Route: Deletes a specific student using their unique ID."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        
    flash(f"Student {student_id} was successfully removed.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)