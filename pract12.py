import sqlite3

# Подключение к базе
db = sqlite3.connect('university.db')
sql = db.cursor()

# Создаем табличку если ее нет
sql.execute('''CREATE TABLE IF NOT EXISTS students 
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                last_name TEXT,
                group_num TEXT,
                mark1 INTEGER,
                mark2 INTEGER,
                mark3 INTEGER,
                mark4 INTEGER)''')
db.commit()


def add():
    print("\nДобавляем студента")
    n = input("Имя: ")
    ln = input("Фамилия: ")
    gr = input("Группа: ")
    print("4 оценки через пробел:")
    m1, m2, m3, m4 = map(int, input().split())

    sql.execute("INSERT INTO students (name, last_name, group_num, mark1, mark2, mark3, mark4) VALUES (?,?,?,?,?,?,?)",
                (n, ln, gr, m1, m2, m3, m4))
    db.commit()
    print("Готово!")


def show_all():
    print("\nВсе студенты:")
    sql.execute("SELECT id, name, last_name, group_num FROM students")
    for student in sql.fetchall():
        print(f"{student[0]}. {student[1]} {student[2]} из {student[3]}")


def show_one():
    num = input("\nНомер студента: ")
    sql.execute("SELECT name, last_name, group_num, mark1, mark2, mark3, mark4 FROM students WHERE id=?", (num,))
    res = sql.fetchone()

    if res:
        avg = (res[3] + res[4] + res[5] + res[6]) / 4
        print(f"\n{res[0]} {res[1]}")
        print(f"Группа: {res[2]}")
        print(f"Оценки: {res[3]}, {res[4]}, {res[5]}, {res[6]}")
        print(f"Средний: {avg:.1f}")
    else:
        print("Нет такого!")


def change():
    num = input("\nНомер студента для изменения: ")
    print("Новые данные (если не меняем - просто Enter):")

    n = input("Имя: ")
    ln = input("Фамилия: ")
    gr = input("Группа: ")
    marks = input("4 оценки через пробел: ")

    if n:
        sql.execute("UPDATE students SET name=? WHERE id=?", (n, num))
    if ln:
        sql.execute("UPDATE students SET last_name=? WHERE id=?", (ln, num))
    if gr:
        sql.execute("UPDATE students SET group_num=? WHERE id=?", (gr, num))
    if marks:
        m1, m2, m3, m4 = map(int, marks.split())
        sql.execute("UPDATE students SET mark1=?, mark2=?, mark3=?, mark4=? WHERE id=?",
                    (m1, m2, m3, m4, num))

    db.commit()
    print("Изменено!")


def delete():
    num = input("\nНомер студента для удаления: ")
    sql.execute("DELETE FROM students WHERE id=?", (num,))
    db.commit()
    print("Удалено!")


def group_avg():
    gr = input("\nГруппа: ")
    sql.execute("SELECT AVG((mark1+mark2+mark3+mark4)/4.0) FROM students WHERE group_num=?", (gr,))
    res = sql.fetchone()[0]
    print(f"Средний балл: {res:.1f}" if res else "Нет такой группы")


# Главное меню
while True:
    print("\n1 - Добавить")
    print("2 - Все студенты")
    print("3 - Найти по номеру")
    print("4 - Изменить")
    print("5 - Удалить")
    print("6 - Средний группы")
    print("0 - Выход")

    c = input("Выберите: ")

    if c == "1":
        add()
    elif c == "2":
        show_all()
    elif c == "3":
        show_one()
    elif c == "4":
        change()
    elif c == "5":
        delete()
    elif c == "6":
        group_avg()
    elif c == "0":
        db.close()
        print("Пока!")
        break
    else:
        print("Не понял...")