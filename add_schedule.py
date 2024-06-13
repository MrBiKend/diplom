import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkcalendar import Calendar

def connect():
    return sqlite3.connect('duss.db')

def add_schedule(class_id, student_id, class_date, class_time):
    if check_coach_availability(class_id, class_date, class_time):
        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO schedule (class_id, student_id, class_date, class_time) VALUES (?, ?, ?, ?)",
                    (class_id, student_id, class_date, class_time))
        conn.commit()
        conn.close()
    else:
        messagebox.showerror("Ошибка", "Тренер занят в это время.")

def check_coach_availability(class_id, class_date, class_time):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT coaches.coach_id FROM schedule "
                "JOIN classes ON schedule.class_id = classes.class_id "
                "JOIN coaches ON classes.coach_id = coaches.coach_id "
                "WHERE classes.class_id=? AND schedule.class_date=? AND schedule.class_time=?",
                (class_id, class_date, class_time))
    result = cur.fetchone()
    conn.close()
    return result is None

def add_schedule_window():
    def submit():
        class_id = get_class_id(class_combobox.get())
        student_id = get_student_id(student_combobox.get())
        class_date = cal.get_date()
        class_time = time_combobox.get()
        add_schedule(class_id, student_id, class_date, class_time)
        messagebox.showinfo("Успех", "Расписание добавлено успешно!")
        window.destroy()

    window = CTk()
    window.title("Добавить расписание")

    class_label = CTkLabel(window, text="Занятие")
    class_label.pack(pady=10)
    class_combobox = CTkComboBox(window, values=get_classes_list())
    class_combobox.pack(pady=10)

    student_label = CTkLabel(window, text="Студент")
    student_label.pack(pady=10)
    student_combobox = CTkComboBox(window, values=get_students_list())
    student_combobox.pack(pady=10)

    class_date_label = CTkLabel(window, text="Дата занятия")
    class_date_label.pack(pady=10)
    cal = Calendar(window, selectmode="day")
    cal.pack(pady=10)

    class_time_label = CTkLabel(window, text="Время занятия")
    class_time_label.pack(pady=10)
    time_combobox = CTkComboBox(window, values=["1 урок", "2 урок", "3 урок", "4 урок", "5 урок", "6 урок", "7 урок", "8 урок", "9 урок", "10 урок"])
    time_combobox.pack(pady=10)

    submit_button = CTkButton(window, text="Добавить", command=submit)
    submit_button.pack(pady=10)

    window.mainloop()

def get_classes_list():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT class_name FROM classes")
    classes = [row[0] for row in cur.fetchall()]
    conn.close()
    return classes

def get_students_list():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT first_name || ' ' || last_name FROM students")
    students = [row[0] for row in cur.fetchall()]
    conn.close()
    return students

def get_class_id(class_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT class_id FROM classes WHERE class_name=?", (class_name,))
    class_id = cur.fetchone()[0]
    conn.close()
    return class_id

def get_student_id(student_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT student_id FROM students WHERE first_name || ' ' || last_name=?", (student_name,))
    student_id = cur.fetchone()[0]
    conn.close()
    return student_id
