class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = float(rate)  # Преобразуем ставку в число
        self.days = int(days)  # Преобразуем количество дней в число

    def GetSalary(self):  # Исправлено имя метода
        salary = self.rate * self.days
        return salary

    def __str__(self):
        return f"{self.name} {self.surname}, Зарплата: {self.GetSalary()}"

worker_1 = Worker("Лиза", "Редькина", "200", "10")
print(worker_1)
