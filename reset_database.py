from db import get_connection

connection = get_connection()

connection.execute(
    "DELETE FROM students"
)

connection.commit()
connection.close()

print("All student records deleted.")