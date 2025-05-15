class Counter:
    def __init__(self, start=8):
        self._value = start

    def __add__(self, other):
        return Counter(self._value + other)

    def __sub__(self, other):
        return Counter(self._value - other)

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


c1 = Counter()
print(f"Начальное значение: {c1}")
max_counter = c1 + 1
print(f"После увелечения на 1: {max_counter}")
min_counter = c1 - 1
print(f"После уменьшения на 1: {min_counter}")
