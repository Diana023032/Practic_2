import sqlite3

class I_Love_Drink:
    def __init__(self, db_name = "love_drink"):
        self.con = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.con.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Drinks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            is_alcoholic BOOLEAN,
            price REAL,
            strength REAL,
            volume REAL CHECK (volume >= 0))
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            quantity INTEGER CHECK (quantity >= 0))
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cocktails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                strength REAL,
                price REAL
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cocktail_Components (
                cocktail_id INTEGER,
                component_type TEXT,
                component_name TEXT,
                quantity REAL,
                FOREIGN KEY (cocktail_id) REFERENCES Cocktails(id)
            )""")

    def add_cocktail(self, name, price, components):
        """Добавление коктейля в склад"""
        cursor = self.con.cursor()
        total_alcohol = 0.0
        total_volume = 0.0
        for component in components:
            type_ = component['type']
            name_ = component['name']
            quantity = component['quantity']
            if type_ == 'Drink':
                cursor.execute("SELECT is_alcoholic, strength FROM Drinks WHERE name = ?", (name_,))
                drink = cursor.fetchone()
                if not drink:
                    print(f"Напиток {name_} не найден!")
                    return
                if drink[0]:  # is_alcoholic
                    total_alcohol += drink[1] * quantity
                    total_volume += quantity
            elif type_ == 'Ingredient':
                cursor.execute("SELECT 1 FROM Ingredients WHERE name = ?", (name_,))
                if not cursor.fetchone():
                    print(f"Ингредиент {name_} не найден!")
                    return
        strength = total_alcohol / total_volume if total_volume > 0 else 0
        try:
            # Сначала добавляем коктейль в таблицу Cocktails
            cursor.execute("INSERT INTO Cocktails (name, strength, price) VALUES (?, ?, ?)",
                           (name, strength, price))
            cocktail_id = cursor.lastrowid  # Получаем ID только что добавленного коктейля

            # Затем добавляем компоненты
            for component in components:
                cursor.execute("""INSERT INTO Cocktail_Components 
                               (cocktail_id, component_type, component_name, quantity)
                               VALUES (?, ?, ?, ?)""",
                               (cocktail_id, component['type'], component['name'], component['quantity']))
            self.con.commit()  # Не забываем подтверждать изменения
            print("Коктейль успешно добавлен!")
        except sqlite3.IntegrityError:
            print("Коктейль с таким именем уже существует!")

    def add_drink(self, name, price, is_alcoholic, volume, strength):
        """Добавление напитка в склад"""
        cursor = self.con.cursor()
        cursor.execute("""
                        INSERT INTO Drinks 
                        (name,price,strength,volume,is_alcoholic)
                        VALUES (?, ?, ?, ?, ?)
                        """, (
            name,
            price,
            strength,
            volume,
            is_alcoholic
        ))
        self.con.commit()

    def add_ingredient(self, name, quantity):
        """Добавление ингредиента в склад"""
        cursor = self.con.cursor()
        cursor.execute("""
                        INSERT INTO Ingredients 
                        (name, quantity)
                        VALUES (?, ?)
                        """, (
            name,
            quantity
        ))
        self.con.commit()

    def sell_cocktail(self, name):
        """Продажа коктейлей"""
        cursor = self.con.cursor()
        cursor.execute("SELECT id FROM Cocktails WHERE name = ?", (name,))
        cocktail = cursor.fetchone()
        if not cocktail:
            print("Коктейль не найден!")
            return
        cursor.execute("""SELECT component_type, component_name, quantity 
                       FROM Cocktail_Components WHERE cocktail_id = ?""", (cocktail[0],))
        components = cursor.fetchall()
        for component in components:
            type_, name_, quantity = component
            if type_ == 'Drink':
                cursor.execute("SELECT volume FROM Drinks WHERE name = ?", (name_,))
                volume = cursor.fetchone()[0]
                if volume < quantity:
                    print(f"Напитка {name_} нет в наличии!")
                    return
            elif type_ == 'Ingredient':
                cursor.execute("SELECT quantity FROM Ingredients WHERE name = ?", (name_,))
                ingredient = cursor.fetchone()[0]
                if ingredient < quantity:
                    print(f"Ингредиента {name_} в наличии нет!")
                    return
        try:
            for component in components:
                type_, name_, quantity = component
                if type_ == 'Drink':
                    cursor.execute("UPDATE Drinks SET volume = volume - ? WHERE name = ?",
                                   (quantity, name_))
                elif type_ == 'Ingredient':
                    cursor.execute("UPDATE Ingredients SET quantity = quantity - ? WHERE name = ?",
                                   (quantity, name_))
            self.con.commit()  # Добавлено
            print("Продажа завершена.")
        except:
            self.con.rollback()  # Откатываем изменения при ошибке
            print("Ошибка при продаже.")

    def show_cocktails(self):
        """Вывод информации о всех коктейлях"""
        cursor = self.con.cursor()

        cursor.execute("SELECT * FROM Cocktails")
        cocktails = cursor.fetchall()

        print("Список коктейлей:")
        for cocktail in cocktails:
            print(f"Название: {cocktail[1]}\n"
                  f"Крепость: {cocktail[2]}%\n"
                  f"Цена: {cocktail[3]}")

            cursor.execute("""SELECT component_type, component_name, quantity 
                           FROM Cocktail_Components WHERE cocktail_id = ?""", (cocktail[0],))
            components = cursor.fetchall()
            print("Состав:")
            for comp in components:
                print(f"- {comp[1]} ({comp[2]})")
        print()
    def restock(self, item_type, name, amount):
        """Пополняет запасы ингредиента или напитка"""
        cursor = self.con.cursor()
        try:
            if item_type == 'ingredient':
                cursor.execute("""
                    UPDATE Ingredients SET quantity = quantity + ? 
                    WHERE name = ?""", (amount, name))
            elif item_type == 'drink':
                cursor.execute("""
                    UPDATE Drinks SET volume = volume + ? 
                    WHERE name = ?""", (amount, name))
            else:
                print("Неверный тип предмета")
                return False

            if cursor.rowcount == 0:
                print(f"{name} не найден!")
                return False

            self.con.commit()
            print(f"Запасы {name} успешно пополнены!")
            return True
        except Exception as e:
            self.con.rollback()
            print(f"Ошибка при пополнении запасов: {str(e)}")
            return False

    def show_inventory(self):
        """Показывает текущие остатки"""
        cursor = self.con.cursor()

        print("\nОстатки напитков:")
        cursor.execute("SELECT name, volume FROM Drinks")
        for row in cursor.fetchall():
            print(f"- {row[0]}: {row[1]} мл")

        print("\nОстатки ингредиентов:")
        cursor.execute("SELECT name, quantity FROM Ingredients")
        for row in cursor.fetchall():
            print(f"- {row[0]}: {row[1]} шт.")
        print()

    def sell_drink(self, name, volume):
        """Продажа напитка"""
        cursor = self.con.cursor()
        try:
            cursor.execute("""
                UPDATE Drinks SET volume = volume - ? 
                WHERE name = ? AND volume >= ?""",
                           (volume, name, volume))

            if cursor.rowcount == 0:
                print("Недостаточно напитка в наличии или напиток не найден!")
                return False

            self.con.commit()
            print(f"Продано {volume} мл {name}")
            return True
        except Exception as e:
            self.con.rollback()
            print(f"Ошибка при продаже: {str(e)}")
            return False

if __name__ == "__main__":
    print("Приложение 'I Love Drink'\n")
    bar = I_Love_Drink()
    while True:
        print("1 - Добавить ингредиент\n"
              "2 - Добавить коктейль\n"
              "3 - Добавить напиток\n"
              "4 - Продать коктейль\n"
              "5 - Продать напиток\n"
              "6 - Пополнить запасы\n"
              "7 - Показать остатки\n"
              "8 - Показать коктейли\n"
              "9 - Выход")
        action = int(input("Выберите действие: "))
        match action:
            case 1:
                name = input("Введите название ингредиента: ").lower()
                quantity = int(input("Введите кол-во ингредиента: "))
                bar.add_ingredient(name, quantity)

            case 2:
                name = input("Название коктейля: ").lower()
                price = float(input("Цена коктейля: "))
                components = []
                while True:
                    print("Добавить компонент:\n"
                          "1 - Алкогольный напиток\n"
                          "2 - Ингредиент\n"
                          "3 - Закончить ввод\n")
                    choice = input("ввод: ")
                    choice = int(choice)
                    if choice == 1:
                        drink = input("Название напитка: ").lower()
                        volume = float(input("Объем напитка: "))
                        components.append({'type': 'Drink', 'name': drink, 'quantity': volume})
                    elif choice == 2:
                        ing = input("Название ингредиента: ").lower()
                        count = float(input("Количество: "))
                        components.append({'type': 'Ingredient', 'name': ing, 'quantity': count})
                    elif choice == 3:
                        break
                    else:
                        print("Некорректный ввод!")
                bar.add_cocktail(name, price, components)

            case 3:
                name = input("Введите название напитка: ").lower()
                price = float(input("Введите цену за 100 мл напитка: "))
                volume = float(input("Введите начальный объём напитка: "))
                is_alcoholic = input("Напиток алкогольный (+/-) ")
                if is_alcoholic == "+":
                    strength = float(input("Введите крепость напитка: "))
                    bar.add_drink(name, price, True, volume, strength)
                elif is_alcoholic == "-":
                    bar.add_drink(name, price, False, volume, None)
                else:
                    print("Ошибка ввода")

            case 4:
                name = input("Название коктейля для продажи: ").lower()
                bar.sell_cocktail(name)

            case 5:
                name_sell = input("Введите название напитка для продажи: ").lower()
                volume_sell = float(input("Введите объём продажи: "))

            case 6:
                stocks = input("Какие запасы необходимо пополнить (1 - Ингредиенты, 2 - Напитки): ")
                stocks = int(stocks)
                if stocks == 1:
                    ingredient = input("Введите название ингредиента: ")
                    ingredient_adding = int(input("Введите кол-во пополнения: "))
                    bar.restock('ingredient', ingredient, ingredient_adding)
                elif stocks == 2:
                    drink = input("Введите название напитка: ")
                    volume_adding = int(input("Введите объём пополнения: "))
                    bar.restock('drink', drink, volume_adding)
                else:
                    print("Ошибка ввода")
            case 7:
                bar.show_inventory()

            case 8:
                bar.show_cocktails()

            case 9:
                print("Программа завершена")
                bar.close()
                break

            case _:
                print("Действие не выбрано")