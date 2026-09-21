def create_item(item_id, name, year, condition, price):
    return {
        "id": item_id,
        "name": name,
        "year": year,
        "condition": condition,
        "price": price,
    }


def get_total_value(items):
    return sum(item["price"] for item in items)


def find_item_by_name(items, query):
    return [i for i in items if query.lower() in i["name"].lower()]


def show_items(items):
    if not items:
        print("\nКоллекция пуста.")
        return
    print("\nID   | Название             | Год   | Состояние  | Цена (руб.)")
    print("-" * 58)
    for i in items:
        print(
            f"{i['id']:<4} | {i['name'][:20]:<20} | {i['year']:<5} | "
            f"{i['condition'][:10]:<10} | {i['price']:<10.2f}"
        )


def main():
    items = [
        create_item(1, "1 рубль 1898 года", 1898, "Отличное", 15000.0),
        create_item(2, "Винил The Beatles", 1969, "Хорошее", 4500.0),
        create_item(3, "Марка Космос СССР", 1961, "Идеальное", 2200.0),
    ]

    while True:
        print("\n=== Личная коллекция (ПР1) ===")
        print("1. Показать все предметы")
        print("2. Добавить предмет")
        print("3. Общая стоимость коллекции")
        print("4. Поиск по названию")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_items(items)
        elif choice == "2":
            name = input("Название: ").strip()
            if not name:
                print("Название не может быть пустым.")
                continue
            try:
                year = int(input("Год выпуска: ").strip())
                price = float(input("Оценочная стоимость (руб.): ").strip())
            except ValueError:
                print("Некорректный ввод числа.")
                continue
            condition = input("Состояние: ").strip()
            new_id = max([i["id"] for i in items], default=0) + 1
            item = create_item(new_id, name, year, condition, price)
            items.append(item)
            print(f"Предмет «{name}» успешно добавлен под ID {new_id}!")
        elif choice == "3":
            total = get_total_value(items)
            print(f"\nОбщая оценочная стоимость коллекции: {total:,.2f} руб.")
        elif choice == "4":
            query = input("Введите текст для поиска: ").strip()
            results = find_item_by_name(items, query)
            show_items(results)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
