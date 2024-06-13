import sqlite3
from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox, ttk
from tkcalendar import Calendar

# Импортируем модули для добавления данных
import add_student
import add_coach
import add_class
import add_schedule

# Подключение к базе данных
def connect():
    return sqlite3.connect('duss.db')

# Функции для работы с базой данных
def add_student_db(first_name, last_name, date_of_birth, enrollment_date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (first_name, last_name, date_of_birth, enrollment_date) VALUES (?, ?, ?, ?)",
                (first_name, last_name, date_of_birth, enrollment_date))
    conn.commit()
    conn.close()

def get_students():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_student(student_id, first_name, last_name, date_of_birth, enrollment_date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE students SET first_name=?, last_name=?, date_of_birth=?, enrollment_date=? WHERE student_id=?",
                (first_name, last_name, date_of_birth, enrollment_date, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()

def add_coach_db(first_name, last_name, specialty):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO coaches (first_name, last_name, specialty) VALUES (?, ?, ?)",
                (first_name, last_name, specialty))
    conn.commit()
    conn.close()

def get_coaches():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM coaches")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_coach(coach_id, first_name, last_name, specialty):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE coaches SET first_name=?, last_name=?, specialty=? WHERE coach_id=?",
                (first_name, last_name, specialty, coach_id))
    conn.commit()
    conn.close()

def delete_coach(coach_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM coaches WHERE coach_id=?", (coach_id,))
    conn.commit()
    conn.close()

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

def update_class(class_id, class_name, coach_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE classes SET class_name=?, coach_id=? WHERE class_id=?",
                (class_name, coach_id, class_id))
    conn.commit()
    conn.close()

def delete_class(class_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM classes WHERE class_id=?", (class_id,))
    conn.commit()
    conn.close()

def add_schedule_db(class_id, student_id, class_date, class_time):
    if check_coach_availability(class_id, class_date, class_time):
        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO schedule (class_id, student_id, class_date, class_time) VALUES (?, ?, ?, ?)",
                    (class_id, student_id, class_date, class_time))
        conn.commit()
        conn.close()
    else:
        messagebox.showerror("Ошибка", "Тренер занят в это время.")

def get_schedule():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT schedule.schedule_id, classes.class_name, students.first_name, students.last_name, schedule.class_date, schedule.class_time FROM schedule LEFT JOIN classes ON schedule.class_id = classes.class_id LEFT JOIN students ON schedule.student_id = students.student_id")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_schedule(schedule_id, class_id, student_id, class_date, class_time):
    if check_coach_availability(class_id, class_date, class_time):
        conn = connect()
        cur = conn.cursor()
        cur.execute("UPDATE schedule SET class_id=?, student_id=?, class_date=?, class_time=? WHERE schedule_id=?",
                    (class_id, student_id, class_date, class_time, schedule_id))
        conn.commit()
        conn.close()
    else:
        messagebox.showerror("Ошибка", "Тренер занят в это время.")

def delete_schedule(schedule_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM schedule WHERE schedule_id=?", (schedule_id,))
    conn.commit()
    conn.close()

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

def add_group_db(group_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO groups (group_name) VALUES (?)", (group_name,))
    conn.commit()
    conn.close()

def get_groups():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM groups")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_group(group_id, group_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE groups SET group_name=? WHERE group_id=?", (group_name, group_id))
    conn.commit()
    conn.close()

def delete_group(group_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM groups WHERE group_id=?", (group_id,))
    conn.commit()
    conn.close()

def add_diary_entry_db(group_id, entry_date, entry_content):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO diaries (group_id, entry_date, entry_content) VALUES (?, ?, ?)",
                (group_id, entry_date, entry_content))
    conn.commit()
    conn.close()

def get_diary_entries(group_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM diaries WHERE group_id=?", (group_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_diary_entry(entry_id, entry_date, entry_content):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE diaries SET entry_date=?, entry_content=? WHERE entry_id=?",
                (entry_date, entry_content, entry_id))
    conn.commit()
    conn.close()

def delete_diary_entry(entry_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM diaries WHERE entry_id=?", (entry_id,))
    conn.commit()
    conn.close()

# Пример интерфейса на customtkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление спортивной школой")

        # Настройка стиля
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', background='#2E2E2E', foreground='white', rowheight=25, fieldbackground='#2E2E2E')
        self.style.map('Treeview', background=[('selected', '#347083')])

        self.login_window()

    def login_window(self):
        self.clear_window()

        self.username_label = ctk.CTkLabel(self.main_frame, text="Логин")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self.main_frame)
        self.username_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(self.main_frame, text="Пароль")
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.main_frame, text="Войти", command=self.check_login)
        self.login_button.pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "director" and password == "1212":
            self.main_menu()
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    def main_menu(self):
        self.clear_window()

        self.menu_frame = ctk.CTkFrame(self.main_frame)
        self.menu_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.students_button = ctk.CTkButton(self.menu_frame, text="Студенты", command=self.view_students_window)
        self.students_button.pack(pady=10)

        self.coaches_button = ctk.CTkButton(self.menu_frame, text="Тренеры", command=self.view_coaches_window)
        self.coaches_button.pack(pady=10)

        self.classes_button = ctk.CTkButton(self.menu_frame, text="Занятия", command=self.view_classes_window)
        self.classes_button.pack(pady=10)

        self.schedule_button = ctk.CTkButton(self.menu_frame, text="Расписание", command=self.schedule_menu)
        self.schedule_button.pack(pady=10)

    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_student_window(self):
        add_student.add_student_window()

    def view_students_window(self):
        self.clear_window()

        self.students_tree = ttk.Treeview(self.main_frame, columns=("Имя", "Фамилия", "Дата рождения", "Дата зачисления"), show="headings")
        self.students_tree.heading("Имя", text="Имя")
        self.students_tree.heading("Фамилия", text="Фамилия")
        self.students_tree.heading("Дата рождения", text="Дата рождения")
        self.students_tree.heading("Дата зачисления", text="Дата зачисления")
        self.students_tree.pack(fill=BOTH, expand=True)

        self.students_tree.bind("<Double-1>", self.on_student_double_click)

        students = get_students()
        for student in students:
            self.students_tree.insert("", "end", values=(student[1], student[2], student[3], student[4]))

        self.add_student_button = ctk.CTkButton(self.main_frame, text="Добавить студента", command=self.add_student_window)
        self.add_student_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def on_student_double_click(self, event):
        item = self.students_tree.selection()[0]
        student_data = self.students_tree.item(item, "values")
        self.edit_student_window(student_data)

    def edit_student_window(self, student_data):
        self.clear_window()

        self.first_name_label = ctk.CTkLabel(self.main_frame, text="Имя")
        self.first_name_label.pack(pady=10)
        self.first_name_entry = ctk.CTkEntry(self.main_frame)
        self.first_name_entry.insert(0, student_data[0])
        self.first_name_entry.pack(pady=10)

        self.last_name_label = ctk.CTkLabel(self.main_frame, text="Фамилия")
        self.last_name_label.pack(pady=10)
        self.last_name_entry = ctk.CTkEntry(self.main_frame)
        self.last_name_entry.insert(0, student_data[1])
        self.last_name_entry.pack(pady=10)

        self.dob_label = ctk.CTkLabel(self.main_frame, text="Дата рождения")
        self.dob_label.pack(pady=10)
        self.dob_entry = ctk.CTkEntry(self.main_frame)
        self.dob_entry.insert(0, student_data[2])
        self.dob_entry.pack(pady=10)

        self.enrollment_label = ctk.CTkLabel(self.main_frame, text="Дата зачисления")
        self.enrollment_label.pack(pady=10)
        self.enrollment_entry = ctk.CTkEntry(self.main_frame)
        self.enrollment_entry.insert(0, student_data[3])
        self.enrollment_entry.pack(pady=10)

        self.update_button = ctk.CTkButton(self.main_frame, text="Обновить студента", command=lambda: self.update_student(student_data[0]))
        self.update_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self.main_frame, text="Удалить студента", command=lambda: self.delete_student(student_data[0]))
        self.delete_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def update_student(self, student_id):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        date_of_birth = self.dob_entry.get()
        enrollment_date = self.enrollment_entry.get()
        update_student(student_id, first_name, last_name, date_of_birth, enrollment_date)
        messagebox.showinfo("Успех", "Студент обновлен успешно!")

    def delete_student(self, student_id):
        delete_student(student_id)
        messagebox.showinfo("Успех", "Студент удален успешно!")
        self.main_menu()

    def add_coach_window(self):
        add_coach.add_coach_window()

    def view_coaches_window(self):
        self.clear_window()

        self.coaches_tree = ttk.Treeview(self.main_frame, columns=("Имя", "Фамилия", "Специальность"), show="headings")
        self.coaches_tree.heading("Имя", text="Имя")
        self.coaches_tree.heading("Фамилия", text="Фамилия")
        self.coaches_tree.heading("Специальность", text="Специальность")
        self.coaches_tree.pack(fill=BOTH, expand=True)

        self.coaches_tree.bind("<Double-1>", self.on_coach_double_click)

        coaches = get_coaches()
        for coach in coaches:
            self.coaches_tree.insert("", "end", values=(coach[1], coach[2], coach[3]))

        self.add_coach_button = ctk.CTkButton(self.main_frame, text="Добавить тренера", command=self.add_coach_window)
        self.add_coach_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def on_coach_double_click(self, event):
        item = self.coaches_tree.selection()[0]
        coach_data = self.coaches_tree.item(item, "values")
        self.edit_coach_window(coach_data)

    def edit_coach_window(self, coach_data):
        self.clear_window()

        self.first_name_label = ctk.CTkLabel(self.main_frame, text="Имя")
        self.first_name_label.pack(pady=10)
        self.first_name_entry = ctk.CTkEntry(self.main_frame)
        self.first_name_entry.insert(0, coach_data[0])
        self.first_name_entry.pack(pady=10)

        self.last_name_label = ctk.CTkLabel(self.main_frame, text="Фамилия")
        self.last_name_label.pack(pady=10)
        self.last_name_entry = ctk.CTkEntry(self.main_frame)
        self.last_name_entry.insert(0, coach_data[1])
        self.last_name_entry.pack(pady=10)

        self.specialty_label = ctk.CTkLabel(self.main_frame, text="Специальность")
        self.specialty_label.pack(pady=10)
        self.specialty_entry = ctk.CTkEntry(self.main_frame)
        self.specialty_entry.insert(0, coach_data[2])
        self.specialty_entry.pack(pady=10)

        self.update_button = ctk.CTkButton(self.main_frame, text="Обновить тренера", command=lambda: self.update_coach(coach_data[0]))
        self.update_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self.main_frame, text="Удалить тренера", command=lambda: self.delete_coach(coach_data[0]))
        self.delete_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def update_coach(self, coach_id):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        specialty = self.specialty_entry.get()
        update_coach(coach_id, first_name, last_name, specialty)
        messagebox.showinfo("Успех", "Тренер обновлен успешно!")

    def delete_coach(self, coach_id):
        delete_coach(coach_id)
        messagebox.showinfo("Успех", "Тренер удален успешно!")
        self.main_menu()

    def add_class_window(self):
        add_class.add_class_window()

    def view_classes_window(self):
        self.clear_window()

        self.classes_tree = ttk.Treeview(self.main_frame, columns=("Название занятия", "Тренер"), show="headings")
        self.classes_tree.heading("Название занятия", text="Название занятия")
        self.classes_tree.heading("Тренер", text="Тренер")
        self.classes_tree.pack(fill=BOTH, expand=True)

        self.classes_tree.bind("<Double-1>", self.on_class_double_click)

        classes = get_classes()
        for cls in classes:
            self.classes_tree.insert("", "end", values=(cls[1], f"{cls[2]} {cls[3]}"))

        self.add_class_button = ctk.CTkButton(self.main_frame, text="Добавить занятие", command=self.add_class_window)
        self.add_class_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def on_class_double_click(self, event):
        item = self.classes_tree.selection()[0]
        class_data = self.classes_tree.item(item, "values")
        self.edit_class_window(class_data)

    def edit_class_window(self, class_data):
        self.clear_window()

        self.class_name_label = ctk.CTkLabel(self.main_frame, text="Название занятия")
        self.class_name_label.pack(pady=10)
        self.class_name_entry = ctk.CTkEntry(self.main_frame)
        self.class_name_entry.insert(0, class_data[0])
        self.class_name_entry.pack(pady=10)

        self.coach_label = ctk.CTkLabel(self.main_frame, text="Тренер")
        self.coach_label.pack(pady=10)
        self.coach_combobox = ctk.CTkComboBox(self.main_frame, values=self.get_coaches_list())
        self.coach_combobox.set(class_data[1])
        self.coach_combobox.pack(pady=10)

        self.update_button = ctk.CTkButton(self.main_frame, text="Обновить занятие", command=lambda: self.update_class(class_data[0]))
        self.update_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self.main_frame, text="Удалить занятие", command=lambda: self.delete_class(class_data[0]))
        self.delete_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def get_coaches_list(self):
        coaches = get_coaches()
        coaches_list = []
        for coach in coaches:
            coaches_list.append(f"{coach[1]} {coach[2]}")
        return coaches_list

    def update_class(self, class_id):
        class_name = self.class_name_entry.get()
        coach_name = self.coach_combobox.get()
        coach_id = self.get_coach_id(coach_name)
        update_class(class_id, class_name, coach_id)
        messagebox.showinfo("Успех", "Занятие обновлено успешно!")

    def delete_class(self, class_id):
        delete_class(class_id)
        messagebox.showinfo("Успех", "Занятие удалено успешно!")
        self.main_menu()

    def schedule_menu(self):
        self.clear_window()

        self.schedule_students_button = ctk.CTkButton(self.main_frame, text="Расписание студентов", command=self.view_students_schedule_window)
        self.schedule_students_button.pack(pady=10)

        self.schedule_coaches_button = ctk.CTkButton(self.main_frame, text="Расписание тренеров", command=self.view_coaches_schedule_window)
        self.schedule_coaches_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def add_schedule_window(self):
        add_schedule.add_schedule_window()

    def view_students_schedule_window(self):
        self.clear_window()

        self.schedule_tree = ttk.Treeview(self.main_frame, columns=("Класс", "Студент", "Дата", "Время"), show="headings")
        self.schedule_tree.heading("Класс", text="Класс")
        self.schedule_tree.heading("Студент", text="Студент")
        self.schedule_tree.heading("Дата", text="Дата")
        self.schedule_tree.heading("Время", text="Время")
        self.schedule_tree.pack(fill=BOTH, expand=True)

        self.schedule_tree.bind("<Double-1>", self.on_schedule_double_click)

        schedules = get_schedule()
        for schedule in schedules:
            self.schedule_tree.insert("", "end", values=(schedule[1], f"{schedule[2]} {schedule[3]}", schedule[4], schedule[5]))

        self.add_schedule_button = ctk.CTkButton(self.main_frame, text="Добавить расписание", command=self.add_schedule_window)
        self.add_schedule_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в меню расписаний", command=self.schedule_menu)
        self.back_button.pack(pady=10)

    def view_coaches_schedule_window(self):
        self.clear_window()

        self.schedule_tree = ttk.Treeview(self.main_frame, columns=("Класс", "Тренер", "Дата", "Время"), show="headings")
        self.schedule_tree.heading("Класс", text="Класс")
        self.schedule_tree.heading("Тренер", text="Тренер")
        self.schedule_tree.heading("Дата", text="Дата")
        self.schedule_tree.heading("Время", text="Время")
        self.schedule_tree.pack(fill=BOTH, expand=True)

        self.schedule_tree.bind("<Double-1>", self.on_schedule_double_click_coach)

        schedules = get_schedule()
        for schedule in schedules:
            coach_name = f"{schedule[2]} {schedule[3]}"
            self.schedule_tree.insert("", "end", values=(schedule[1], coach_name, schedule[4], schedule[5]))

        self.add_schedule_button = ctk.CTkButton(self.main_frame, text="Добавить расписание", command=self.add_schedule_window)
        self.add_schedule_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в меню расписаний", command=self.schedule_menu)
        self.back_button.pack(pady=10)

    def on_schedule_double_click(self, event):
        item = self.schedule_tree.selection()[0]
        schedule_data = self.schedule_tree.item(item, "values")
        self.edit_schedule_window(schedule_data)

    def on_schedule_double_click_coach(self, event):
        item = self.schedule_tree.selection()[0]
        schedule_data = self.schedule_tree.item(item, "values")
        self.edit_schedule_window(schedule_data)

    def edit_schedule_window(self, schedule_data):
        self.clear_window()

        self.class_label = ctk.CTkLabel(self.main_frame, text="Занятие")
        self.class_label.pack(pady=10)
        self.class_combobox = ctk.CTkComboBox(self.main_frame, values=self.get_classes_list())
        self.class_combobox.set(schedule_data[0])
        self.class_combobox.pack(pady=10)

        self.student_label = ctk.CTkLabel(self.main_frame, text="Студент")
        self.student_label.pack(pady=10)
        self.student_combobox = ctk.CTkComboBox(self.main_frame, values=self.get_students_list())
        self.student_combobox.set(schedule_data[1])
        self.student_combobox.pack(pady=10)

        self.class_date_label = ctk.CTkLabel(self.main_frame, text="Дата занятия")
        self.class_date_label.pack(pady=10)
        self.cal = Calendar(self.main_frame, selectmode="day")
        self.cal.set_date(schedule_data[2])
        self.cal.pack(pady=10)

        self.class_time_label = ctk.CTkLabel(self.main_frame, text="Время занятия")
        self.class_time_label.pack(pady=10)
        self.time_combobox = ctk.CTkComboBox(self.main_frame, values=["1 урок", "2 урок", "3 урок", "4 урок", "5 урок", "6 урок", "7 урок", "8 урок", "9 урок", "10 урок"])
        self.time_combobox.set(schedule_data[3])
        self.time_combobox.pack(pady=10)

        self.update_button = ctk.CTkButton(self.main_frame, text="Обновить расписание", command=lambda: self.update_schedule(schedule_data[0]))
        self.update_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self.main_frame, text="Удалить расписание", command=lambda: self.delete_schedule(schedule_data[0]))
        self.delete_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.main_frame, text="Вернуться в главное меню", command=self.main_menu)
        self.back_button.pack(pady=10)

    def update_schedule(self, schedule_id):
        class_id = self.get_class_id(self.class_combobox.get())
        student_id = self.get_student_id(self.student_combobox.get())
        class_date = self.cal.get_date()
        class_time = self.time_combobox.get()
        update_schedule(schedule_id, class_id, student_id, class_date, class_time)
        messagebox.showinfo("Успех", "Расписание обновлено успешно!")

    def delete_schedule(self, schedule_id):
        delete_schedule(schedule_id)
        messagebox.showinfo("Успех", "Расписание удалено успешно!")
        self.main_menu()

root = ctk.CTk()
root.geometry("1300x600")
app = App(root)
root.mainloop()
