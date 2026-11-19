\
import sqlite3

print("COURSE REGISTRATION DATABASE")

# Establish database connection
conn = sqlite3.connect("university.db")
c = conn.cursor()

# Enable foreign key constraints
c.execute("PRAGMA foreign_keys = ON")


# 1. Creating courses table
def create_courses_table():
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS courses(
                courseCode TEXT PRIMARY KEY,
                courseName TEXT NOT NULL,
                units INTEGER NOT NULL
            )
        """)

        conn.commit()
        print("Courses table created successfully.")

    except sqlite3.Error as e:
        print("Error creating courses table:", e)


# 2. Creating students table
def create_students_table():
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                Department TEXT NOT NULL,
                courseCode TEXT REFERENCES courses(courseCode),
                Level TEXT NOT NULL,
                email TEXT NOT NULL,
                yearOfBirth INTEGER NOT NULL
            )
        """)

        conn.commit()
        print("Students table created successfully.")

    except sqlite3.Error as e:
        print("Error creating students table:", e)


# 3. Registering courses
def register_courses():
    try:
        choice = int(input("How many courses do you want to register? "))

        if choice <= 0:
            print("Enter a positive number of courses.")
            return

        count = 0

        while count < choice:
            print(f"\nRegistering course {count + 1}")

            course_code = input("Enter course code: ")
            course_name = input("Enter course name: ")
            units = int(input("Enter number of units: "))

            if units <= 0:
                print("Course units must be positive.")
                continue

            try:
                c.execute("""
                    INSERT INTO courses
                    (courseCode, courseName, units)
                    VALUES (?, ?, ?)
                """, (course_code, course_name, units))

                conn.commit()
                count += 1
                print("Course registered successfully.")

            except sqlite3.IntegrityError as e:
                print("Course registration failed:", e)

    except ValueError:
        print("Invalid input. Enter numbers where required.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 4. Registering students for courses
def register_student_for_course():
    try:
        choice = int(input("How many students do you want to register? "))

        if choice <= 0:
            print("Enter a positive number of students.")
            return

        count = 0

        while count < choice:
            print(f"\nRegistering student {count + 1}")

            student_id = int(input("Enter student ID: "))
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            department = input("Enter department: ")
            course_code = input("Enter course code: ")
            level = input("Enter level: ")
            email = input("Enter email: ")
            year_of_birth = int(input("Enter year of birth: "))

            try:
                c.execute("""
                    INSERT INTO students
                    (id, firstName, lastName, Department,
                    courseCode, Level, email, yearOfBirth)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    student_id, first_name, last_name,
                    department, course_code, level,
                    email, year_of_birth
                ))

                conn.commit()
                count += 1
                print("Student registered successfully.")

            except sqlite3.IntegrityError as e:
                print("Student registration failed:", e)

    except ValueError:
        print("Invalid input. Enter numbers for ID and year of birth.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 5. Retrieving student and course information
def retrieve_student_and_course_info():
    try:
        choice = input(
            "Retrieve student or course information? "
            "(student/course): "
        ).lower()

        if choice == "student":
            student_id = int(input("Enter student ID: "))

            c.execute(
                "SELECT * FROM students WHERE id = ?",
                (student_id,)
            )

            student_info = c.fetchone()

            if student_info:
                print("\nSTUDENT INFORMATION")
                print("ID:", student_info[0])
                print("First Name:", student_info[1])
                print("Last Name:", student_info[2])
                print("Department:", student_info[3])
                print("Course Code:", student_info[4])
                print("Level:", student_info[5])
                print("Email:", student_info[6])
                print("Year of Birth:", student_info[7])

            else:
                print("Student not found.")

        elif choice == "course":
            course_code = input("Enter course code: ")

            c.execute(
                "SELECT * FROM courses WHERE courseCode = ?",
                (course_code,)
            )

            course_info = c.fetchone()

            if course_info:
                print("\nCOURSE INFORMATION")
                print("Course Code:", course_info[0])
                print("Course Name:", course_info[1])
                print("Units:", course_info[2])

            else:
                print("Course not found.")

        else:
            print("Invalid choice. Enter student or course.")

    except ValueError:
        print("Invalid input. Enter a valid student ID.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 6. Searching for students and courses
def search_information():
    try:
        choice = input(
            "Search for student or course? (student/course): "
        ).lower()

        if choice == "student":
            keyword = input("Enter student name to search: ")

            c.execute("""
                SELECT * FROM students
                WHERE firstName LIKE ? OR lastName LIKE ?
            """, ('%' + keyword + '%', '%' + keyword + '%'))

            results = c.fetchall()

            if results:
                print("\nSEARCH RESULTS")

                for student in results:
                    print("--------------------------")
                    print("ID:", student[0])
                    print("Name:", student[1], student[2])
                    print("Department:", student[3])
                    print("Course Code:", student[4])
                    print("Level:", student[5])

            else:
                print("No matching students found.")

        elif choice == "course":
            keyword = input("Enter course name or code: ")

            c.execute("""
                SELECT * FROM courses
                WHERE courseName LIKE ? OR courseCode LIKE ?
            """, ('%' + keyword + '%', '%' + keyword + '%'))

            results = c.fetchall()

            if results:
                print("\nSEARCH RESULTS")

                for course in results:
                    print("--------------------------")
                    print("Course Code:", course[0])
                    print("Course Name:", course[1])
                    print("Units:", course[2])

            else:
                print("No matching courses found.")

        else:
            print("Invalid choice.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 7. Modifying student information
def modify_student():
    try:
        student_id = int(input("Enter student ID to modify: "))

        c.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = c.fetchone()

        if student:
            print("\nEnter the new student information.")

            first_name = input("Enter new first name: ")
            last_name = input("Enter new last name: ")
            department = input("Enter new department: ")
            course_code = input("Enter new course code: ")
            level = input("Enter new level: ")
            email = input("Enter new email: ")
            year_of_birth = int(input("Enter new year of birth: "))

            c.execute("""
                UPDATE students
                SET firstName = ?,
                    lastName = ?,
                    Department = ?,
                    courseCode = ?,
                    Level = ?,
                    email = ?,
                    yearOfBirth = ?
                WHERE id = ?
            """, (
                first_name, last_name, department,
                course_code, level, email,
                year_of_birth, student_id
            ))

            conn.commit()
            print("Student information updated successfully.")

        else:
            print("Student not found.")

    except ValueError:
        print("Invalid numerical input.")

    except sqlite3.IntegrityError as e:
        print("Modification failed:", e)

    except sqlite3.Error as e:
        print("Database error:", e)


# 8. Modifying course information
def modify_course():
    try:
        course_code = input("Enter course code to modify: ")

        c.execute(
            "SELECT * FROM courses WHERE courseCode = ?",
            (course_code,)
        )

        course = c.fetchone()

        if course:
            print("\nEnter new course information.")

            course_name = input("Enter new course name: ")
            units = int(input("Enter new number of units: "))

            if units <= 0:
                print("Course units must be positive.")
                return

            c.execute("""
                UPDATE courses
                SET courseName = ?, units = ?
                WHERE courseCode = ?
            """, (course_name, units, course_code))

            conn.commit()
            print("Course information updated successfully.")

        else:
            print("Course not found.")

    except ValueError:
        print("Invalid input. Units must be a number.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 9. Deleting student records
def delete_student():
    try:
        student_id = int(input("Enter student ID to delete: "))

        c.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = c.fetchone()

        if student:
            confirm = input(
                f"Delete {student[1]} {student[2]}? (yes/no): "
            )

            if confirm.lower() == "yes":
                c.execute(
                    "DELETE FROM students WHERE id = ?",
                    (student_id,)
                )

                conn.commit()
                print("Student record deleted successfully.")

            else:
                print("Deletion cancelled.")

        else:
            print("Student not found.")

    except ValueError:
        print("Invalid student ID.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 10. Deleting course records
def delete_course():
    try:
        course_code = input("Enter course code to delete: ")

        c.execute(
            "SELECT * FROM courses WHERE courseCode = ?",
            (course_code,)
        )

        course = c.fetchone()

        if course:
            confirm = input(
                f"Delete {course[1]}? (yes/no): "
            )

            if confirm.lower() == "yes":
                c.execute(
                    "DELETE FROM courses WHERE courseCode = ?",
                    (course_code,)
                )

                conn.commit()
                print("Course deleted successfully.")

            else:
                print("Deletion cancelled.")

        else:
            print("Course not found.")

    except sqlite3.IntegrityError:
        print(
            "Cannot delete this course because students "
            "are registered for it."
        )

    except sqlite3.Error as e:
        print("Database error:", e)


# 11. Demonstrating student-course relationship
def relationship_demonstration():
    try:
        c.execute("""
            SELECT students.firstName,
                   students.lastName,
                   courses.courseCode,
                   courses.courseName
            FROM students
            JOIN courses
            ON students.courseCode = courses.courseCode
        """)

        student_course_info = c.fetchall()

        print("\nSTUDENT AND COURSE INFORMATION")

        if student_course_info:
            for row in student_course_info:
                print(
                    f"{row[0]} {row[1]} offers "
                    f"{row[2]} - {row[3]}"
                )
        else:
            print("No student-course relationships found.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 12. Main menu
def main():
    create_courses_table()
    create_students_table()

    while True:
        print("\n========== COURSE REGISTRATION MENU ==========")
        print("1. Register courses")
        print("2. Register students")
        print("3. Retrieve student/course information")
        print("4. Search for students/courses")
        print("5. Modify student information")
        print("6. Modify course information")
        print("7. Delete student records")
        print("8. Delete course records")
        print("9. Demonstrate student-course relationship")
        print("10. Exit")

        try:
            choice = int(input("\nEnter your choice: "))

            if choice == 1:
                register_courses()

            elif choice == 2:
                register_student_for_course()

            elif choice == 3:
                retrieve_student_and_course_info()

            elif choice == 4:
                search_information()

            elif choice == 5:
                modify_student()

            elif choice == 6:
                modify_course()

            elif choice == 7:
                delete_student()

            elif choice == 8:
                delete_course()

            elif choice == 9:
                relationship_demonstration()

            elif choice == 10:
                print("Thank you for using the Course Registration Database.")
                break

            else:
                print("Invalid choice. Select between 1 and 10.")

        except ValueError:
            print("Please enter a valid number.")


# Execute program
if __name__ == "__main__":
    try:
        main()

    finally:
        conn.close()
