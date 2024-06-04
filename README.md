### README

# Управление спортивной школой

Это приложение для управления спортивной школой, написанное на языке Python с использованием библиотеки Tkinter для создания графического интерфейса пользователя и базы данных PostgreSQL для хранения данных.

## Требования

- Python 3.x
- PostgreSQL
- Библиотеки Python:
  - psycopg2
  - tkcalendar

## Установка

1. Установите Python 3.x, если он еще не установлен.
2. Установите PostgreSQL и создайте базу данных `sports_school`.
3. Установите необходимые библиотеки Python:
    ```bash
    pip install psycopg2 tkcalendar
    ```

4. Создайте таблицы в базе данных, используя скрипт ниже.

## Скрипт для создания базы данных

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    enrollment_date DATE NOT NULL
);

CREATE TABLE coaches (
    coach_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL
);

CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    coach_id INTEGER REFERENCES coaches(coach_id)
);

CREATE TABLE schedule (
    schedule_id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(class_id),
    student_id INTEGER REFERENCES students(student_id),
    class_date DATE NOT NULL,
    class_time VARCHAR(50) NOT NULL
);
```

## Запуск

1. Клонируйте репозиторий или скопируйте файлы проекта в рабочую директорию.
2. Запустите скрипт с графическим интерфейсом:
    ```bash
    python main.py
    ```

## Описание

Программа предоставляет следующие функции:

### Студенты
- Добавление нового студента.
- Просмотр списка студентов.
- Обновление информации о студенте.
- Удаление студента.

### Тренеры
- Добавление нового тренера.
- Просмотр списка тренеров.
- Обновление информации о тренере.
- Удаление тренера.

### Занятия
- Добавление нового занятия.
- Просмотр списка занятий.
- Обновление информации о занятии.
- Удаление занятия.

### Расписание
- Добавление нового расписания.
- Просмотр расписания.
- Обновление расписания.
- Удаление расписания.

## Интерфейс

### Главное меню
Главное меню программы содержит пункты для управления студентами, тренерами, занятиями и расписанием.

### Пример интерфейса для добавления студента

![Добавление студента](https://via.placeholder.com/600x400)

### Пример интерфейса для просмотра списка студентов

![Просмотр списка студентов](https://via.placeholder.com/600x400)

## Контакты

Если у вас возникли вопросы или предложения, вы можете связаться с нами по адресу электронной почты: support@example.com.

---

### Скрипт для создания базы данных в SQLShell

Сохраните следующий скрипт в файл, например `create_database.sql`, и выполните его в SQLShell (psql) для создания необходимых таблиц в базе данных `sports_school`:

```sql
-- Подключение к базе данных
\c sports_school

-- Создание таблицы студентов
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    enrollment_date DATE NOT NULL
);

-- Создание таблицы тренеров
CREATE TABLE coaches (
    coach_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL
);

-- Создание таблицы занятий
CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    coach_id INTEGER REFERENCES coaches(coach_id)
);

-- Создание таблицы расписания
CREATE TABLE schedule (
    schedule_id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(class_id),
    student_id INTEGER REFERENCES students(student_id),
    class_date DATE NOT NULL,
    class_time VARCHAR(50) NOT NULL
);
```

Для выполнения скрипта в SQLShell, используйте команду:
```bash
psql -U postgres -f create_database.sql
```

GoogleDisk: https://drive.google.com/drive/folders/1pbg3wC7-6FY5WmUwVEwn8fdC-f9dUij9?usp=sharing
