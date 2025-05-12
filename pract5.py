class Train:
    def __init__(self, destination, number, time):
        self.destination = destination
        self.number = number
        self.time = time

    def __str__(self):
        return f"Поезд: {self.number}\n"\
               f"Место направление: {self.destination}\n"\
               f"Время: {self.time}"

trains = [
        Train("Томск", "348", "10:50"),
        Train("Омск", "456", "11:30"),
        Train("Новокузнецк", "347", "16:00"),
    ]
number = input("Введите номер поезда для получения информации: ")

found_train = None
for train in trains:
    if train.number == number:
        found_train = train
        break

if found_train:
    print(found_train)
else:
    print("Поезд не найден")
