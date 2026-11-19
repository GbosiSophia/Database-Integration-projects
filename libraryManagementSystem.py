
import sqlite3

print("LIBRARY DATABASE APPLICATION")

# Establish database connection
conn = sqlite3.connect("library.db")
c = conn.cursor()


# 1. Create books table
def create_books_table():
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS books(
                bookID INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT NOT NULL,
                yearPublished INTEGER NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        conn.commit()
        print("Books table created successfully.")

    except sqlite3.Error as e:
        print("Error creating table:", e)


# 2. Book registration
def register_book():
    try:
        book_id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter author's name: ")
        publisher = input("Enter publisher: ")
        year = int(input("Enter year published: "))
        category = input("Enter book category: ")
        quantity = int(input("Enter quantity: "))

        if quantity < 0:
            print("Quantity cannot be negative.")
            return

        c.execute("""
            INSERT INTO books
            (bookID, title, author, publisher, yearPublished, category, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (book_id, title, author, publisher, year, category, quantity))

        conn.commit()
        print("Book registered successfully.")

    except ValueError:
        print("Invalid input. Enter numbers for ID, year and quantity.")

    except sqlite3.IntegrityError as e:
        print("Registration failed. Book ID may already exist:", e)

    except sqlite3.Error as e:
        print("Database error:", e)


# 3. Book retrieval
def retrieve_book():
    try:
        book_id = int(input("Enter book ID to retrieve: "))

        c.execute(
            "SELECT * FROM books WHERE bookID = ?",
            (book_id,)
        )

        book = c.fetchone()

        if book:
            print("\nBOOK INFORMATION")
            print("Book ID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("Publisher:", book[3])
            print("Year Published:", book[4])
            print("Category:", book[5])
            print("Quantity:", book[6])
        else:
            print("Book not found.")

    except ValueError:
        print("Invalid book ID. Enter a number.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 4. Book searching
def search_book():
    try:
        keyword = input("Enter book title or author to search: ")

        c.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ?
        """, ('%' + keyword + '%', '%' + keyword + '%'))

        books = c.fetchall()

        if books:
            print("\nSEARCH RESULTS")
            for book in books:
                print("--------------------------")
                print("Book ID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("Publisher:", book[3])
                print("Year Published:", book[4])
                print("Category:", book[5])
                print("Quantity:", book[6])
        else:
            print("No matching books found.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 5. Book modification
def modify_book():
    try:
        book_id = int(input("Enter book ID to modify: "))

        c.execute(
            "SELECT * FROM books WHERE bookID = ?",
            (book_id,)
        )

        book = c.fetchone()

        if book:
            print("\nEnter the new book information.")

            title = input("Enter new title: ")
            author = input("Enter new author: ")
            publisher = input("Enter new publisher: ")
            year = int(input("Enter new year published: "))
            category = input("Enter new category: ")
            quantity = int(input("Enter new quantity: "))

            if quantity < 0:
                print("Quantity cannot be negative.")
                return

            c.execute("""
                UPDATE books
                SET title = ?,
                    author = ?,
                    publisher = ?,
                    yearPublished = ?,
                    category = ?,
                    quantity = ?
                WHERE bookID = ?
            """, (title, author, publisher, year,
                  category, quantity, book_id))

            conn.commit()
            print("Book information updated successfully.")

        else:
            print("Book not found. Cannot modify.")

    except ValueError:
        print("Invalid input. Check the numerical fields.")

    except sqlite3.Error as e:
        print("Database error:", e)


# 6. Book deletion
def delete_book():
    try:
        book_id = int(input("Enter book ID to delete: "))

        c.execute(
            "SELECT * FROM books WHERE bookID = ?",
            (book_id,)
        )

        book = c.fetchone()

        if book:
            confirm = input(
                f"Are you sure you want to delete '{book[1]}'? (yes/no): "
            )

            if confirm.lower() == "yes":
                c.execute(
                    "DELETE FROM books WHERE bookID = ?",
                    (book_id,)
                )

                conn.commit()
                print("Book deleted successfully.")
            else:
                print("Deletion cancelled.")

        else:
            print("Book not found.")

    except ValueError:
        print("Invalid book ID. Enter a number.")

    except sqlite3.Error as e:
        print("Database error:", e)


# Main menu
def main():
    create_books_table()

    while True:
        print("\n========== LIBRARY MENU ==========")
        print("1. Register a book")
        print("2. Retrieve a book")
        print("3. Search for a book")
        print("4. Modify book information")
        print("5. Delete a book")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                register_book()

            elif choice == 2:
                retrieve_book()

            elif choice == 3:
                search_book()

            elif choice == 4:
                modify_book()

            elif choice == 5:
                delete_book()

            elif choice == 6:
                print("Thank you for using the Library Database.")
                break

            else:
                print("Invalid choice. Select between 1 and 6.")

        except ValueError:
            print("Please enter a valid number.")


    conn.close()
    
if __name__ == "__main__":
    main()

