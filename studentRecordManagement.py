print("====STUDENT RECORD MANAGEMENT SYSTEM====")
import sqlite3
conn = sqlite3.connect("university.db")
c = conn.cursor()

#students table
c.execute("""CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    Department TEXT NOT NULL,
    Level TEXT NOT NULL,
    email TEXT NOT NULL,
    yearOfBirth TEXT NOT NULL)""")

print("Students table created successfully.")
conn.commit()

#inserting student records
student_records = [
    (1001, "John", "Adewale", "Computer Science", "100","john.doe@example.com", "2000"),
    (1002, "Jane", "Smith", "Mathematics", "300","jane.smith@example.com", "1999"),
    (1003, "Alice", "Johnson", "Computer Science", "200","alice.johnson@example.com", "2001"),
    (1004, "Bob", "Williams", "Chemistry", "400","bob.williams@example.com", "2000"),
    (1005, "Emily", "Brown", "Biology", "300","emily.brown@example.com", "1998")
]

# for record in student_records:
c.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?)", student_records)
print("Student records inserted successfully.")
conn.commit()

#Retrieve all student records
c.execute("SELECT * FROM students")
student_records = c.fetchall()

for record in student_records:
    print(record)
print("All student records retrieved successfully.")

# retrieving students from a specific department
c.execute("SELECT * FROM students WHERE Department = ?", ("Computer Science",))
department_students = c.fetchall()
print("Students from Computer Science department:")

for record in department_students:
    print(record)

# Updating a students level
c.execute("""UPDATE students SET Level = ? WHERE id = ? """, ("200", 1001))
print("Student record updated successfully.")

conn.commit()

# Deleting a student record
c.execute("DELETE FROM students WHERE id = ?", (1005,))

print("Student record deleted successfully.")
conn.commit()

conn.close()
