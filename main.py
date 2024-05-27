import psycopg2
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import Calendar



# Подключение к базе данных
def connect():
    return psycopg2.connect(
        database="sports_school",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

# Функции для работы с базой данных

# Функции для работы со студентами
def add_student(first_name, last_name, date_of_birth, enrollment_date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (first_name, last_name, date_of_birth, enrollment_date) VALUES (%s, %s, %s, %s)",
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
    cur.execute("UPDATE students SET first_name=%s, last_name=%s, date_of_birth=%s, enrollment_date=%s WHERE student_id=%s",
                (first_name, last_name, date_of_birth, enrollment_date, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    conn.commit()
    conn.close()

# Функции для работы с тренерами
def add_coach(first_name, last_name, specialty):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO coaches (first_name, last_name, specialty) VALUES (%s, %s, %s)",
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
    cur.execute("UPDATE coaches SET first_name=%s, last_name=%s, specialty=%s WHERE coach_id=%s",
                (first_name, last_name, specialty, coach_id))
    conn.commit()
    conn.close()

def delete_coach(coach_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM coaches WHERE coach_id=%s", (coach_id,))
    conn.commit()
    conn.close()

# Функции для работы с занятиями
def add_class(class_name, coach_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO classes (class_name, coach_id) VALUES (%s, %s)", (class_name, coach_id))
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
    cur.execute("UPDATE classes SET class_name=%s, coach_id=%s WHERE class_id=%s",
                (class_name, coach_id, class_id))
    conn.commit()
    conn.close()

def delete_class(class_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM classes WHERE class_id=%s", (class_id,))
    conn.commit()
    conn.close()

# Функции для работы с расписанием
def add_schedule(class_id, student_id, class_date, class_time):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO schedule (class_id, student_id, class_date, class_time) VALUES (%s, %s, %s, %s)",
                (class_id, student_id, class_date, class_time))
    conn.commit()
    conn.close()

def get_schedule():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT schedule.schedule_id, classes.class_name, students.first_name, students.last_name, schedule.class_date, schedule.class_time FROM schedule LEFT JOIN classes ON schedule.class_id = classes.class_id LEFT JOIN students ON schedule.student_id = students.student_id")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_schedule(schedule_id, class_id, student_id, class_date, class_time):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE schedule SET class_id=%s, student_id=%s, class_date=%s, class_time=%s WHERE schedule_id=%s",
                (class_id, student_id, class_date, class_time, schedule_id))
    conn.commit()
    conn.close()

def delete_schedule(schedule_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM schedule WHERE schedule_id=%s", (schedule_id,))
    conn.commit()
    conn.close()

# Пример интерфейса на Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление спортивной школой")

        # Создание меню
        menu = Menu(root)
        root.config(menu=menu)

        students_menu = Menu(menu)
        menu.add_cascade(label="Группы", menu=students_menu)
        students_menu.add_command(label="Добавить", command=self.add_student_window)
        students_menu.add_separator()
        students_menu.add_command(label="Просмотреть", command=self.view_students_window)

        coaches_menu = Menu(menu)
        menu.add_cascade(label="Тренеры", menu=coaches_menu)
        coaches_menu.add_command(label="Добавить", command=self.add_coach_window)
        coaches_menu.add_separator()
        coaches_menu.add_command(label="Просмотреть", command=self.view_coaches_window)

        classes_menu = Menu(menu)
        menu.add_cascade(label="Занятия", menu=classes_menu)
        classes_menu.add_command(label="Добавить", command=self.add_class_window)
        classes_menu.add_separator()
        classes_menu.add_command(label="Просмотреть", command=self.view_classes_window)

        schedule_menu = Menu(menu)
        menu.add_cascade(label="Расписание", menu=schedule_menu)
        schedule_menu.add_command(label="Добавить", command=self.add_schedule_window)
        schedule_menu.add_separator()
        schedule_menu.add_command(label="Просмотреть", command=self.view_schedule_window)

    def add_student_window(self):
        self.clear_window()

        self.first_name_label = Label(self.root, text="Название класса")
        self.first_name_label.pack()
        self.first_name_entry = Entry(self.root)
        self.first_name_entry.pack()

        self.last_name_label = Label(self.root, text="Количество студентов")
        self.last_name_label.pack()
        self.last_name_entry = Entry(self.root)
        self.last_name_entry.pack()

        self.dob_label = Label(self.root, text="Приоритет")
        self.dob_label.pack()
        self.dob_entry = Entry(self.root)
        self.dob_entry.pack()

        self.enrollment_label = Label(self.root, text="доп.описание")
        self.enrollment_label.pack()
        self.enrollment_entry = Entry(self.root)
        self.enrollment_entry.pack()

        self.add_button = Button(self.root, text="Добавить студента", command=self.add_student)
        self.add_button.pack()

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def add_student(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        date_of_birth = self.dob_entry.get()
        enrollment_date = self.enrollment_entry.get()
        add_student(first_name, last_name, date_of_birth, enrollment_date)
        messagebox.showinfo("Успех", "Студент добавлен успешно!")

        #Тест


    def view_students_window(self):
        self.clear_window()

        self.students_list = Listbox(self.root)
        self.students_list.pack(fill=BOTH, expand=1)
        students = get_students()
        for student in students:
            self.students_list.insert(END, student)

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def add_coach_window(self):
        self.clear_window()

        self.first_name_label = Label(self.root, text="Имя")
        self.first_name_label.pack()
        self.first_name_entry = Entry(self.root)
        self.first_name_entry.pack()

        self.last_name_label = Label(self.root, text="Фамилия")
        self.last_name_label.pack()
        self.last_name_entry = Entry(self.root)
        self.last_name_entry.pack()

        self.specialty_label = Label(self.root, text="Специальность")
        self.specialty_label.pack()
        self.specialty_entry = Entry(self.root)
        self.specialty_entry.pack()

        self.add_button = Button(self.root, text="Добавить тренера", command=self.add_coach)
        self.add_button.pack()

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def add_coach(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        specialty = self.specialty_entry.get()
        add_coach(first_name, last_name, specialty)
        messagebox.showinfo("Успех", "Тренер добавлен успешно!")

    def view_coaches_window(self):
        self.clear_window()

        self.coaches_list = Listbox(self.root)
        self.coaches_list.pack(fill=BOTH, expand=1)
        coaches = get_coaches()
        for coach in coaches:
            self.coaches_list.insert(END, coach)

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def add_class_window(self):
        self.clear_window()

        self.class_name_label = Label(self.root, text="Название занятия")
        self.class_name_label.pack()
        self.class_name_entry = Entry(self.root)
        self.class_name_entry.pack()

        self.coach_id_label = Label(self.root, text="ID тренера")
        self.coach_id_label.pack()
        self.coach_id_entry = Entry(self.root)
        self.coach_id_entry.pack()

        self.add_button = Button(self.root, text="Добавить занятие", command=self.add_class)
        self.add_button.pack()

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def add_class(self):
        class_name = self.class_name_entry.get()
        coach_id = self.coach_id_entry.get()
        add_class(class_name, coach_id)
        messagebox.showinfo("Успех", "Занятие добавлено успешно!")

    def view_classes_window(self):
        self.clear_window()

        self.classes_list = Listbox(self.root)
        self.classes_list.pack(fill=BOTH, expand=1)
        classes = get_classes()
        for cls in classes:
            self.classes_list.insert(END, cls)

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def add_schedule_window(self):
        self.clear_window()

        self.class_label = Label(self.root, text="Занятие")
        self.class_label.pack()
        self.class_combobox = Combobox(self.root, values=self.get_classes_list())
        self.class_combobox.pack()

        self.student_label = Label(self.root, text="Студент")
        self.student_label.pack()
        self.student_combobox = Combobox(self.root, values=self.get_students_list())
        self.student_combobox.pack()

        self.class_date_label = Label(self.root, text="Дата занятия")
        self.class_date_label.pack()
        self.cal = Calendar(self.root, selectmode="day", year=2022, month=5, day=22)
        self.cal.pack()

        self.class_time_label = Label(self.root, text="Время занятия")
        self.class_time_label.pack()
        self.time_combobox = Combobox(self.root, values=["1 урок", "2 урок", "3 урок", "4 урок", "5 урок", "6 урок", "7 урок", "8 урок", "9 урок", "10 урок"])
        self.time_combobox.pack()

        self.add_button = Button(self.root, text="Добавить расписание", command=self.add_schedule)
        self.add_button.pack()

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def get_classes_list(self):
        classes = get_classes()
        classes_list = []
        for cls in classes:
            classes_list.append(cls[1])  # добавляем название занятия в список
        return classes_list

    def get_students_list(self):
        students = get_students()
        students_list = []
        for student in students:
            students_list.append(student[1] + " " + student[2])  # добавляем имя и фамилию студента в список
        return students_list

    def get_student_id(self, student_name):
        students = get_students()
        for student in students:
            full_name = student[1] + " " + student[2]  # Составляем полное имя студента из имени и фамилии
            if full_name == student_name:  # Проверяем, соответствует ли полное имя студента заданному
                return student[0]  # Возвращаем идентификатор студента
        return None  # Если студент не найден, возвращаем None

    def get_class_id(self, class_name):
        classes = get_classes()
        for cls in classes:
            if cls[1] == class_name:  # Проверяем, соответствует ли название занятия заданному
                return cls[0]  # Возвращаем идентификатор занятия
        return None  # Если занятие не найдено, возвращаем None

    def add_schedule(self):
        class_id = self.get_class_id(self.class_combobox.get())
        student_id = self.get_student_id(self.student_combobox.get())
        class_date = self.cal.get_date()
        class_time = self.time_combobox.get()
        add_schedule(class_id, student_id, class_date, class_time)
        messagebox.showinfo("Успех", "Расписание добавлено успешно!")

    def view_schedule_window(self):
        self.clear_window()

        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")
        style.map("Treeview",
                  background=[('selected', '#347083')])

        self.schedule_tree = ttk.Treeview(self.root, columns=("Класс", "Студент", "Дата", "Время"), style="Treeview")
        self.schedule_tree.heading("#0", text="ID")
        self.schedule_tree.heading("Класс", text="Класс")
        self.schedule_tree.heading("Студент", text="Студент")
        self.schedule_tree.heading("Дата", text="Дата")
        self.schedule_tree.heading("Время", text="Время")
        self.schedule_tree.pack(fill=BOTH, expand=1)

        schedules = get_schedule()
        for schedule in schedules:
            self.schedule_tree.insert("", "end", text=schedule[0], values=(schedule[1], schedule[2] + " " + schedule[3], schedule[4], schedule[5]))

        self.back_button = Button(self.root, text="Вернуться в главное меню", command=self.show_main_menu)
        self.back_button.pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()
        self.__init__(self.root)

root = Tk()
root.geometry("1300x600")  # Устанавливаем размер окна 800x600 пикселей
app = App(root)
root.mainloop()
