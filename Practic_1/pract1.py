j = "ab"
s = "aabbccd"
count = 0
massiv_j = set(j)  # используем set для быстрого поиска
for stone in s:
    if stone in massiv_j:  # проверяем, есть ли камень в множестве драгоценностей
        count += 1
print(j, s, sep="\n")
print(count)
