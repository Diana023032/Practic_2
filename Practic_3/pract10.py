class Worker:
    def __init__(self, name, surname, rate, days):
        self.__name = name
        self.__surname = surname
        self.__rate = float(rate)
        self.__days = int(days)
    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_rate(self):
        return self.__rate

    def get_days(self):
        return self.__days
    def GetSalary(self):
        salary = self.get_rate() * self.get_days()
        return salary

    def __str__(self):
        return f"{self.get_name()} {self.get_surname()}, Зарплата: {self.GetSalary()}"

worker_1 = Worker("Лиза", "Редькина", "200", "10")
print(worker_1)
