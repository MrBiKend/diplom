import sqlite3
from customtkinter import *
from tkinter import messagebox

def connect():
    return sqlite3.connect('duss.db')

def add_coach(first_name, last_name, specialty):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO coaches (first_name, last_name, specialty) VALUES (?, ?, ?)",
                (first_name, last_name, specialty))
    conn.commit()
    conn.close()

def add_coach_window():
    def submit():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        specialty = specialty_entry.get()
        add_coach(first_name, last_name, specialty)
        messagebox.showinfo("Успех", "Тренер добавлен успешно!")
        window.destroy()

    window = CTk()
    window.title("Добавить тренера")

    first_name_label = CTkLabel(window, text="Имя")
    first_name_label.pack(pady=10)
    first_name_entry = CTkEntry(window)
    first_name_entry.pack(pady=10)

    last_name_label = CTkLabel(window, text="Фамилия")
    last_name_label.pack(pady=10)
    last_name_entry = CTkEntry(window)
    last_name_entry.pack(pady=10)

    specialty_label = CTkLabel(window, text="Специальность")
    specialty_label.pack(pady=10)
    specialty_entry = CTkEntry(window)
    specialty_entry.pack(pady=10)

    submit_button = CTkButton(window, text="Добавить", command=submit)
    submit_button.pack(pady=10)

    window.mainloop()
