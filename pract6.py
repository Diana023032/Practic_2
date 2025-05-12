class Numbers:
    def __init__(self, num1):
        self.num1 = num1

    def __add__(self, other):
        return Numbers(self.num1 + other.num1)

    def __gt__(self, other):
        return self.num1 > other.num1

    def __str__(self):
        return str(self.num1)

    def display(self):
        print(f"Число: {self.num1}")

    def edit(self, new_value):
        self.num1 = new_value
        return print(f"Измененное число: {new_value}")

num1 = Numbers(5)
num2 = Numbers(10)
num1.display()
num2.display()
num1.edit(7)
num2.edit(3)
result_sum = num1 + num2
print(f"Сумма: {result_sum}")

if num1 > num2:
    print(f"Наибольшее значение: {num1}")
else:
    print(f"Наибольшее значение: {num2}")
