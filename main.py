import os
import tkinter as tk
from tkinter import ttk
import sqlite3

root = tk.Tk()
root.title("Student Database")


def create_database():
    try:
        if not os.path.exists("students.db"):
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS students (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                surname TEXT,
                                grade REAL,
                                mail_status TEXT
                            )""")
            conn.commit()
            cursor.close()
            conn.close()
            fill_database()
    except sqlite3.Error as e:
        print("Error creating database:", e)


def fill_database():
    try:
        student_data = [
            (1, "John", "Doe", 4.5, "Mailed"),
            (2, "Jane", "Smith", 3.8, "Graded"),
            (3, "Michael", "Johnson", 4.2, "Not Started"),
            (4, "Emily", "Brown", 3.9, "Completed"),
            (5, "William", "Davis", 4.0, "In Progress")
        ]
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO students (id, name, surname, grade, mail_status) VALUES (?, ?, ?, ?, ?)",
                           student_data)
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print("Error filling database:", e)


def fetch_data():
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except sqlite3.Error as e:
        print("Error fetching data:", e)
        return []


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=row)


def add_new_student_window():
    new_window = tk.Toplevel(root)
    new_window.title("Add New Student")
    name_label = ttk.Label(new_window, text="Name:")
    name_label.pack()
    name_entry = ttk.Entry(new_window)
    name_entry.pack()
    surname_label = ttk.Label(new_window, text="Surname:")
    surname_label.pack()
    surname_entry = ttk.Entry(new_window)
    surname_entry.pack()
    grade_label = ttk.Label(new_window, text="Grade:")
    grade_label.pack()
    grade_entry = ttk.Entry(new_window)
    grade_entry.pack()
    project_status_label = ttk.Label(new_window, text="Mail Status:")
    project_status_label.pack()
    project_status_entry = ttk.Entry(new_window)
    project_status_entry.pack()

    def add_new():
        try:
            new_name = name_entry.get()
            new_surname = surname_entry.get()
            new_grade = grade_entry.get()
            new_mail_status = project_status_entry.get()
            if new_grade and new_grade.replace('.', '', 1).isdigit():
                new_grade = float(new_grade)
                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()
                sql = "INSERT INTO students (name, surname, grade, mail_status) VALUES (?, ?, ?, ?)"
                params = (new_name, new_surname, new_grade, new_mail_status)
                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()
                load_data()
                new_window.destroy()
        except sqlite3.Error as e:
            print("Error adding new student:", e)

    add_button = ttk.Button(new_window, text="Add", command=add_new)
    add_button.pack()

add_button = ttk.Button(root, text="Add New Student", command=add_new_student_window)
add_button.pack()

treeview = ttk.Treeview(root)
treeview["columns"] = ("id", "name", "surname", "grade", "mail_status")
treeview.column("#0", width=0, stretch=tk.NO)
treeview.column("id", anchor=tk.CENTER, width=50)
treeview.column("name", anchor=tk.W, width=100)
treeview.column("surname", anchor=tk.W, width=100)
treeview.column("grade", anchor=tk.CENTER, width=50)
treeview.column("mail_status", anchor=tk.W, width=100)
treeview.heading("#0", text="", anchor=tk.CENTER)
treeview.heading("id", text="ID")
treeview.heading("name", text="Name")
treeview.heading("surname", text="Surname")
treeview.heading("grade", text="Grade")
treeview.heading("mail_status", text="Mail Status")
treeview.pack()


def open_details_window(event):
    selected_item = treeview.focus()
    if selected_item:
        item_data = treeview.item(selected_item)
        item_values = item_data["values"]
        details_window = tk.Toplevel(root)
        details_window.title("Details")
        id_label = ttk.Label(details_window, text="ID:")
        id_label.pack()
        id_entry = ttk.Entry(details_window)
        id_entry.insert(0, item_values[0])
        id_entry.config(state="disabled")
        id_entry.pack()
        name_label = ttk.Label(details_window, text="Name:")
        name_label.pack()
        name_entry = ttk.Entry(details_window)
        name_entry.insert(0, item_values[1])
        name_entry.pack()
        surname_label = ttk.Label(details_window, text="Surname:")
        surname_label.pack()
        surname_entry = ttk.Entry(details_window)
        surname_entry.insert(0, item_values[2])
        surname_entry.pack()
        grade_label = ttk.Label(details_window, text="Grade:")
        grade_label.pack()
        grade_entry = ttk.Entry(details_window)
        grade_entry.insert(0, item_values[3])
        grade_entry.pack()
        project_status_label = ttk.Label(details_window, text="Mail Status:")
        project_status_label.pack()
        project_status_entry = ttk.Entry(details_window)
        project_status_entry.insert(0, item_values[4])
        project_status_entry.pack()

        def delete():
            try:
                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()
                sql = "DELETE FROM students WHERE id = ?"
                params = (id_entry.get(),)
                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()
                load_data()
                details_window.destroy()
            except sqlite3.Error as e:
                print("Error deleting student:", e)

        delete_button = ttk.Button(details_window, text="Delete", command=delete)
        delete_button.pack()

        def update():
            try:
                new_name = name_entry.get()
                new_surname = surname_entry.get()
                new_grade = grade_entry.get()
                new_mail_status = project_status_entry.get()
                if new_grade and new_grade.replace('.', '', 1).isdigit():
                    new_grade = float(new_grade)
                    conn = sqlite3.connect("students.db")
                    cursor = conn.cursor()
                    sql = "UPDATE students SET name=?, surname=?, grade=?, mail_status=? WHERE id=?"
                    params = (new_name, new_surname, new_grade, new_mail_status, id_entry.get())
                    cursor.execute(sql, params)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    load_data()
            except sqlite3.Error as e:
                print("Error updating student:", e)

        update_button = ttk.Button(details_window, text="Update", command=update)
        update_button.pack()


treeview.bind("<Double-1>", open_details_window)
create_database()
load_data()
root.mainloop()
