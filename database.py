import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id TEXT NOT NULL,

    name TEXT NOT NULL,

    age INTEGER NOT NULL,

    programme TEXT NOT NULL,

    level TEXT NOT NULL,

    gpa REAL

)
""")

connection.commit()

connection.close()

print("Database created successfully.")