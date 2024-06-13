import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkcalendar import Calendar

def connect():
    return sqlite3.connect('duss.db')

def add_class_db(class_name, coach_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO classes (class_name, coach_id) VALUES (?, ?)", (class_name, coach_id))
    conn.commit()
    conn.close()

def get_classes():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT classes.class_id, classes.class_name, coaches.first_name, coaches.last_name FROM classes LEFT JOIN coaches ON classes.coach_id = coaches.coach_id")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_coaches_list():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT first_name || ' ' || last_name FROM coaches")
    coaches = [row[0] for row in cur.fetchall()]
    conn.close()
    return coaches

def get_class_id(class_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT class_id FROM classes WHERE class_name=?", (class_name,))
    class_id = cur.fetchone()[0]
    conn.close()
    return class_id

def get_coach_id(coach_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT coach_id FROM coaches WHERE first_name || ' ' || last_name=?", (coach_name,))
    coach_id = cur.fetchone()[0]
    conn.close()
    return coach_id

def add_class_window():
    def submit():
        class_name = class_name_entry.get()
        coach_name = coach_combobox.get()
        coach_id = get_coach_id(coach_name)
        add_class_db(class_name, coach_id)
        messagebox.showinfo("Успех", "Занятие добавлено успешно!")
        window.destroy()

    window = CTk()
    window.title("Добавить занятие")

    class_name_label = CTkLabel(window, text="Название занятия")
    class_name_label.pack(pady=10)
    class_name_entry = CTkEntry(window)
    class_name_entry.pack(pady=10)

    coach_label = CTkLabel(window, text="Тренер")
    coach_label.pack(pady=10)
    coach_combobox = CTkComboBox(window, values=get_coaches_list())
    coach_combobox.pack(pady=10)

    submit_button = CTkButton(window, text="Добавить", command=submit)
    submit_button.pack(pady=10)

    window.mainloop()
