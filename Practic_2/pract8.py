class MyClass:
    def __init__(self, parameter1="По_умолчанию_1", parameter2="По_умолчанию_2"):
        self.parameter1 = parameter1
        self.parameter2 = parameter2

    def display(self):
        print(f"Первый параметр: {self.parameter1}")
        print(f"Второй параметр: {self.parameter2}")

    def __del__(self):
        print(f"Объекты удалены")

myclass = MyClass("Люблю", "Спать")
myclass.display()
myclass_default = MyClass()
myclass_default.display()
myclass.parameter1 = "ЛюБлЮ"
myclass.parameter2 = "СпАтЬ"
myclass.display()
myclass.__del__()
