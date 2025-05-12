class Student:
    def __init__(self, surname, date_of_birth, number, progress):
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.number_group = number
        self.progress = progress

    def __str__(self):
        return f"Фамилия: {self.surname}\n" \
               f"Дата рождения: {self.date_of_birth}\n" \
               f"Номер группы: {self.number}\n" \
               f"Успеваемость: {self.progress}"


def find_student(students, surname, date_of_birth):
    for student in students:
        if student.surname == surname and student.date_of_birth == date_of_birth:
            return student
    return None


students = [
    Student("Васильев", "2008-01-15", "436", [4, 5, 3, 5, 4]),
    Student("Лапочкин", "2007-06-20", "345", [5, 5, 5, 4, 5]),
    Student("Иванов", "2006-03-30", "234", [3, 3, 4, 4, 3]),
]

surname_input = input("Введите фамилию студента: ")
date_of_birth_input = input("Введите дату рождения студента (гггг-мм-дд): ")

student = find_student(students, surname_input, date_of_birth_input)

if student:
    print(student)

    n = input("Хотите изменить фамилию, дату рождения и группу? (y/n): ")
    if n.lower() == 'y':
        student.__surname = input("Введите новую фамилию: ")
        student.__date_of_birth = input("Введите новую дату рождения: ")
        student.__number = input("Введите новый номер группы: ")

        print("Информация о студенте обновлена:")
        print(student)
else:
    print("Студент не найден.")
