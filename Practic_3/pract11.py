class Calculation:
    def __init__(self, num1=""):
        self.num1 = num1

    def SetCalculationLine(self, new_num1):
        self.num1 = new_num1

    def SetLastSymbolCalculationLine(self, num1):
        self.num1 += num1

    def GetCalculationLine(self):
        return self.num1

    def GetLastSymbol(self):
        if self.num1:
            return self.num1[-1]
        return None

    def DeleteLastSymbol(self):
        self.num1 = self.num1[:-1]

calc = Calculation()
calc.SetCalculationLine("20+5")
print(calc.GetCalculationLine())  # Вывод: 20+5

calc.SetLastSymbolCalculationLine("#")
print(calc.GetCalculationLine())  # Вывод добавления символа: 20+5#

print(calc.GetLastSymbol())  # Вывод символа: #
calc.DeleteLastSymbol()
print(calc.GetCalculationLine())  # Вывод после удаления символа: 20+5
