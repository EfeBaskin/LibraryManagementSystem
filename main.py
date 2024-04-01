import sqlite3
import atexit
import customtkinter as ctk
from tkinter import messagebox


def connect_to_database():
    conn = sqlite3.connect('LibraryDB.db')
    return conn


def create_table():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowed_books (
            borrowed_book_id INTEGER PRIMARY KEY,
            book_name TEXT,
            FOREIGN KEY (borrowed_book_id) REFERENCES books(id)
        )
    ''')

    conn.commit()
    conn.close()


def add_book(title):

    if title:

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book added successfully!")

    else:
        messagebox.showerror("Error", "Please enter a book title.")


def display_all(available_box, borrowed_box):

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT title FROM books")
    available_books = cursor.fetchall()

    cursor.execute("SELECT book_name FROM borrowed_books")
    borrowed_books = cursor.fetchall()

    available_books_list = [book[0] for book in available_books]
    available_text = "\n".join(available_books_list)
    available_box.delete(1.0, ctk.END)
    available_box.insert(ctk.END, available_text)

    # Display borrowed books in the right text box
    borrowed_books_list = [book[0] for book in borrowed_books]
    borrowed_text = "\n".join(borrowed_books_list)
    borrowed_box.delete(1.0, ctk.END)
    borrowed_box.insert(ctk.END, borrowed_text)

    conn.close()


def borrow_book(book_title):

    if book_title:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM books WHERE title=?", (book_title,))
        book = cursor.fetchone()

        if book:
            book_id = book[0]
            cursor.execute("INSERT INTO borrowed_books (borrowed_book_id, book_name) VALUES (?, ?)", (book_id, book_title))
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Book borrowed successfully!")

        else:
            messagebox.showerror("Book not found in the library.")

    else:
        messagebox.showerror("Please enter a book title.")


def return_book(book_to_return):

    if book_to_return:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT borrowed_book_id FROM borrowed_books WHERE book_name=?", (book_to_return,))
        book = cursor.fetchone()

        if book:
            book_id = book[0]
            cursor.execute("DELETE FROM borrowed_books WHERE borrowed_book_id=?", (book_id,))
            cursor.execute("INSERT INTO books (title) VALUES (?)", (book_to_return,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Book returned successfully!")

        else:
            messagebox.showerror("Book not found in your borrowed books inventory.")

    else:
        messagebox.showerror("Please enter a book title.")


def delete_all_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books")
    cursor.execute("DELETE FROM borrowed_books")
    conn.commit()
    conn.close()


create_table()
atexit.register(delete_all_data)


class LibraryManagementSystem(ctk.CTk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title("LIBRARY MANAGEMENT SYSTEM")
        self.geometry("1000x500")

        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y)

        self.book_entry_label = ctk.CTkLabel(self.left_frame, text="Enter book title:")
        self.book_entry_label.grid(row=0, column=0, padx=5, pady=5)

        self.book_entry = ctk.CTkEntry(self.left_frame)
        self.book_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_button = ctk.CTkButton(self.left_frame, text="Add Book", command=self.add_book_handler)
        self.add_button.grid(row=1, column=0, columnspan=2, padx=5, pady=(10, 10), sticky="ew")

        self.borrow_button = ctk.CTkButton(self.left_frame, text="Borrow Book", command=self.borrow_book_handler)
        self.borrow_button.grid(row=2, column=0, columnspan=2, padx=5, pady=(10, 10), sticky="ew")

        self.return_button = ctk.CTkButton(self.left_frame, text="Return Book", command=self.return_book_handler)
        self.return_button.grid(row=3, column=0, columnspan=2, padx=5, pady=(10, 10), sticky="ew")

        self.display_button = ctk.CTkButton(self.left_frame, text="Display Books", command=self.display_all_handler)
        self.display_button.grid(row=4, column=0, columnspan=2, padx=5, pady=(10, 10), sticky="ew")

        self.exit_button = ctk.CTkButton(self.left_frame, text="Exit", command=self.quit)
        self.exit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=(10, 10), sticky="ew")

        self.available_books_label = ctk.CTkLabel(self.right_frame, text="Available Books:")
        self.available_books_label.grid(row=0, column=0, padx=5, pady=5)

        self.available_books_box = ctk.CTkTextbox(self.right_frame, width=200, height=400)
        self.available_books_box.grid(row=1, column=0, padx=5, pady=5)

        self.borrowed_books_label = ctk.CTkLabel(self.right_frame, text="Borrowed Books:")
        self.borrowed_books_label.grid(row=0, column=1, padx=5, pady=5)

        self.borrowed_books_box = ctk.CTkTextbox(self.right_frame, width=200, height=400)
        self.borrowed_books_box.grid(row=1, column=1, padx=5, pady=5)

    def add_book_handler(self):
        title = self.book_entry.get()
        add_book(title)
        self.book_entry.delete(0, ctk.END)

    def borrow_book_handler(self):
        title = self.book_entry.get()
        borrow_book(title)
        self.book_entry.delete(0, ctk.END)

    def return_book_handler(self):
        title = self.book_entry.get()
        return_book(title)
        self.book_entry.delete(0, ctk.END)

    def display_all_handler(self):
        display_all(self.available_books_box, self.borrowed_books_box)


app = LibraryManagementSystem()
app.mainloop()
