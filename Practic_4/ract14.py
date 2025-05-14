import psutil
import sqlite3
from datetime import datetime

connect = sqlite3.connect("System_monitor.db")
cursor = connect.cursor()
try:
    cursor.execute("""CREATE TABLE InfoSystem
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    CPU TEXT,
                    RAM TEXT,
                    SWAP TEXT,
                    date TEXT)
                    """)
    connect.commit()
except sqlite3.OperationalError:
    pass
print("Приложение 'Системный монитор' ")
while True:
    print("1 - Мониторинг системы.")
    print("2 - Просмотр сохранёных данных.")
    print("3 - Выход.")
    act = int(input("Выберите действие: "))
    if act == 1:
        RAM = psutil.virtual_memory()
        SWAP = psutil.swap_memory()
        CPU = psutil.cpu_percent()
        print(f"CPU загружен на {CPU}%")
        print(f"Оперативной памяти использованно {round(RAM.used/1073741824,1)} Гб")
        print(f"SWAP использованно {round(SWAP.used/1073741824,1)} Гб\n")
        now = datetime.now()
        date = now.strftime("%Y-%m-%d,%H:%M")
        cursor.execute("""
               INSERT INTO InfoSystem
               (CPU, RAM, SWAP, date)
               VALUES (?, ?, ?, ?)
               """, (
            CPU,
            round(RAM[3] / 1073741824, 1),
            round(SWAP.used/1073741824,1),
            date
        ))
        connect.commit()
    elif act == 2:
        cursor.execute("SELECT * FROM InfoSystem")
        all = cursor.fetchall()
        print("История измерений: ")
        for row in all:
            print(f"CPU загружен на {row[1]}%\n"
                  f"Оперативной памяти использованно: {row[2]} Гб\n"
                  f"SWAP использованно: {row[3]} Гб\n"
                  f"Время измерений: {row[4]}\n")
    elif act == 3:
        break
    else:
        print("Действие не выбранно")
connect.close()