import sqlite3

class Student:
    def __init__(self, name, surname, patronymic, group, grades):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.group = group
        if len(grades) != 4:
            raise ValueError("Успеваемость должна содержать 4 оценки.")
        self.grades = grades

def display():
    cursor.execute("SELECT * FROM Student")
    all_rows = cursor.fetchall()

    print("\nВсе студенты:")
    for row in all_rows:
        print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Отчество: {row[3]}, "
              f"Группа: {row[4]}, Средний балл: {row[5]:.2f}")
    print()

def input_student(return_as=False):
    print("Введите данные студента:")
    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество: ")
    group = input("Группа: ")

    while True:
        grades_input = input("4 оценки (через пробел): ").split()
        grades = [int(grade) for grade in grades_input]
        if len(grades) != 4:
            print("Нужно ввести ровно 4 оценки!")
            continue
        if not all(1 <= grade <= 5 for grade in grades):
            print("Оценки должны быть от 1 до 5!")
            continue
        break

    if return_as:
        return [name, surname, patronymic, group, grades]
    return Student(name, surname, patronymic, group, grades)

def add(student):
    average = sum(student.grades) / len(student.grades)
    cursor.execute("""
        INSERT INTO Student 
        (name, surname, patronymic, groups, average_score)
        VALUES (?, ?, ?, ?, ?)
        """, (
        student.name,
        student.surname,
        student.patronymic,
        student.group,
        average
    ))
    connect.commit()

connect = sqlite3.connect("Student.db")
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Student
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                patronymic TEXT,
                groups TEXT,
                average_score REAL)
                """)
connect.commit()
while True:
    print("\n1 - Добавить нового студента\n"
          "2 - Просмотр всех студентов\n"
          "3 - Просмотр одного студента\n"
          "4 - Редактирование студента\n"
          "5 - Удаление студента\n"
          "6 - Средний балл студентов группы\n"
          "7 - Завершить программу")
    action = int(input("Выберите действие: "))


    if action == 1:
        student = input_student()
        add(student)
        print("Студент успешно добавлен")

    elif action == 2:
        display()

    elif action == 3:
        id_student = int(input("Введите ID студента для вывода: "))
        cursor.execute("SELECT * FROM Student WHERE id = ?", (id_student,))
        row = cursor.fetchone()
        if row:
            print(f"\nИмя: {row[1]}, Фамилия: {row[2]}, Отчество: {row[3]}, "
                    f"Группа: {row[4]}, Средний балл: {row[5]:.2f}\n")
        else:
            print("Студент не найден")

    elif action == 4:
        display()
        id_student = input("Выберите ID студента для редактирования: ")
        cursor.execute("SELECT id FROM Student WHERE id = ?", (id_student,))
        if not cursor.fetchone():
            print("Студент не найден")
            continue
        student_info = input_student(return_as=True)  # Исправлено
        average = sum(student_info[4]) / len(student_info[4])
        cursor.execute("""
            UPDATE Student SET 
            name = ?, 
            surname = ?, 
            patronymic = ?, 
            groups = ?, 
            average_score = ? 
            WHERE id = ?
            """, (
            student_info[0],
            student_info[1],
            student_info[2],
            student_info[3],
            average,
            id_student
        ))
        connect.commit()
        print("Данные обновлены")

    elif action == 5:
        display()
        id_student = input("Выберите ID студента для удаления: ")
        cursor.execute("DELETE FROM Student WHERE id = ?", (id_student,))
        if cursor.rowcount > 0:
            print("Студент удалён!")
        else:
            print("Студент не найден.")
        connect.commit()

    elif action == 6:
        group_number = input("Введите группу для вывода среднего балла: ")
        cursor.execute("SELECT average_score FROM Student WHERE groups = ?", (group_number,))
        rows = cursor.fetchall()
        if not rows:
            print("В этой группе нет студентов")
            continue

        total = sum(row[0] for row in rows)
        average = total / len(rows)
        print(f"Средний балл группы {group_number}: {average:.2f}")

    elif action == 7:
        break

    else:
        print("Неизвестное действие. Введите число от 1 до 7")

connect.close()