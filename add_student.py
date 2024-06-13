import sqlite3
from customtkinter import *
from tkinter import messagebox

def connect():
    return sqlite3.connect('duss.db')

def add_student(first_name, last_name, date_of_birth, enrollment_date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (first_name, last_name, date_of_birth, enrollment_date) VALUES (?, ?, ?, ?)",
                (first_name, last_name, date_of_birth, enrollment_date))
    conn.commit()
    conn.close()

def add_student_window():
    def submit():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        date_of_birth = dob_entry.get()
        enrollment_date = enrollment_entry.get()
        add_student(first_name, last_name, date_of_birth, enrollment_date)
        messagebox.showinfo("Успех", "Студент добавлен успешно!")
        window.destroy()

    window = CTk()
    window.title("Добавить студента")

    first_name_label = CTkLabel(window, text="Имя")
    first_name_label.pack(pady=10)
    first_name_entry = CTkEntry(window)
    first_name_entry.pack(pady=10)

    last_name_label = CTkLabel(window, text="Фамилия")
    last_name_label.pack(pady=10)
    last_name_entry = CTkEntry(window)
    last_name_entry.pack(pady=10)

    dob_label = CTkLabel(window, text="Дата рождения")
    dob_label.pack(pady=10)
    dob_entry = CTkEntry(window)
    dob_entry.pack(pady=10)

    enrollment_label = CTkLabel(window, text="Дата зачисления")
    enrollment_label.pack(pady=10)
    enrollment_entry = CTkEntry(window)
    enrollment_entry.pack(pady=10)

    submit_button = CTkButton(window, text="Добавить", command=submit)
    submit_button.pack(pady=10)

    window.mainloop()
