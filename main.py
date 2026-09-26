from typing import Any
from essence.categories import (
    add_category,
    delete_category,
    find_category_by_id,
)
from essence.collections import (
    add_collection,
    delete_collection,
    find_collection_by_id,
    get_user_collections,
)
from essence.items import (
    add_item,
    check_rarity,
    delete_item,
    get_items_by_collection,
    get_total_value,
    sort_items_by_price,
)
from essence.users import add_user, delete_user, find_user_by_id
from storage import load_data, save_data
from utils import input_float, input_int, input_non_empty

FILES = {
    "users": "data/users.json",
    "categories": "data/categories.json",
    "collections": "data/collections.json",
    "items": "data/items.json",
}


def show_summary(
    users: list[dict[str, Any]],
    categories: list[dict[str, Any]],
    collections: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> None:
    print("\n--- Общая статистика системы ---")
    print(f"Пользователей: {len(users)}")
    print(f"Категорий: {len(categories)}")
    print(f"Коллекций: {len(collections)}")
    print(f"Предметов всего: {len(items)}")
    val = get_total_value(items)
    print(f"Общая оценочная стоимость: {val:,.2f} руб.")


def show_items_detailed(
    items: list[dict[str, Any]],
    categories: list[dict[str, Any]],
) -> None:
    if not items:
        print("\nПредметов нет.")
        return
    header = (
        f"{'ID':<4} | {'Название':<22} | {'Категория':<14} | "
        f"{'Год':<6} | {'Цена':<10} | {'Редкость'}"
    )
    sep = "-" * len(header)
    print("\n" + sep)
    print(header)
    print(sep)
    for i in items:
        cat = find_category_by_id(categories, i["category_id"])
        c_name = cat["name"] if cat else "Без категории"
        rarity = check_rarity(i["year"])
        row = (
            f"{i['id']:<4} | {i['name'][:20]:<22} | {c_name[:12]:<14} | "
            f"{i['year']:<6} | {i['price']:<10.2f} | {rarity}"
        )
        print(row)
    print(sep)


def handle_delete_item(
    items: list[dict[str, Any]],
) -> None:
    if not items:
        print("Список предметов пуст.")
        return
    item_id = input_int("Введите ID предмета для удаления: ", min_val=1)
    if delete_item(items, item_id):
        save_data(FILES["items"], items)
        print(f"Предмет с ID {item_id} успешно удален.")
    else:
        print(f"Предмет с ID {item_id} не найден.")


def handle_delete_collection(
    collections: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> None:
    if not collections:
        print("Список коллекций пуст.")
        return
    col_id = input_int("Введите ID коллекции для удаления: ", min_val=1)
    if delete_collection(collections, col_id):
        save_data(FILES["collections"], collections)
        # Каскадно удаляем связанные предметы
        items[:] = [i for i in items if i["collection_id"] != col_id]
        save_data(FILES["items"], items)
        print(f"Коллекция ID {col_id} и входящие в нее предметы удалены.")
    else:
        print(f"Коллекция с ID {col_id} не найдена.")


def handle_delete_user(
    users: list[dict[str, Any]],
    collections: list[dict[str, Any]],
    items: list[dict[str, Any]],
) -> None:
    if not users:
        print("Список пользователей пуст.")
        return
    u_id = input_int("Введите ID пользователя для удаления: ", min_val=1)
    user_cols = get_user_collections(collections, u_id)
    user_col_ids = {c["id"] for c in user_cols}

    if delete_user(users, u_id):
        save_data(FILES["users"], users)
        # Удаляем коллекции и предметы пользователя
        collections[:] = [c for c in collections if c["id"] not in user_col_ids]
        save_data(FILES["collections"], collections)
        items[:] = [i for i in items if i["collection_id"] not in user_col_ids]
        save_data(FILES["items"], items)
        print(f"Пользователь ID {u_id} и все его данные успешно удалены.")
    else:
        print(f"Пользователь с ID {u_id} не найден.")


def main() -> None:
    users = load_data(FILES["users"])
    categories = load_data(FILES["categories"])
    collections = load_data(FILES["collections"])
    items = load_data(FILES["items"])

    while True:
        print("\n=== Сервис управления личными коллекциями ===")
        print("1. Показать общую статистику")
        print("2. Список пользователей")
        print("3. Добавить пользователя")
        print("4. Список категорий")
        print("5. Добавить категорию")
        print("6. Создать коллекцию")
        print("7. Добавить предмет в коллекцию")
        print("8. Показать все предметы (с сортировкой)")
        print("9. Удалить предмет")
        print("10. Удалить коллекцию")
        print("11. Удалить пользователя")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_summary(users, categories, collections, items)
        elif choice == "2":
            print("\nПользователи:")
            for u in users:
                print(f"ID {u['id']}: {u['username']} ({u['email']})")
        elif choice == "3":
            uname = input_non_empty("Имя пользователя: ")
            email = input_non_empty("Email: ")
            u = add_user(users, uname, email)
            save_data(FILES["users"], users)
            print(f"Пользователь {u['username']} создан под ID {u['id']}.")
        elif choice == "4":
            print("\nКатегории:")
            for c in categories:
                print(f"[{c['id']}] {c['name']} - {c.get('description', '')}")
        elif choice == "5":
            name = input_non_empty("Название категории: ")
            desc = input_non_empty("Описание: ")
            c = add_category(categories, name, desc)
            save_data(FILES["categories"], categories)
            print(f"Категория «{c['name']}» добавлена под ID {c['id']}.")
        elif choice == "6":
            if not users:
                print("Сначала создайте хотя бы одного пользователя!")
                continue
            u_id = input_int("Введите ID владельца: ", min_val=1)
            if not find_user_by_id(users, u_id):
                print("Пользователь с таким ID не найден.")
                continue
            c_name = input_non_empty("Название коллекции: ")
            c_desc = input_non_empty("Описание коллекции: ")
            col = add_collection(collections, u_id, c_name, c_desc)
            save_data(FILES["collections"], collections)
            print(f"Коллекция «{col['name']}» создана под ID {col['id']}.")
        elif choice == "7":
            if not collections:
                print("Сначала создайте коллекцию!")
                continue
            col_id = input_int("ID коллекции: ", min_val=1)
            cat_id = input_int("ID категории: ", min_val=1)
            name = input_non_empty("Название предмета: ")
            year = input_int("Год выпуска: ", min_val=1, max_val=2026)
            cond = input_non_empty("Состояние: ")
            price = input_float("Стоимость (руб.): ", min_val=0.0)
            it = add_item(items, col_id, cat_id, name, year, cond, price)
            save_data(FILES["items"], items)
            print(f"Предмет «{it['name']}» добавлен под ID {it['id']}!")
        elif choice == "8":
            ans: str = input("Сортировать по убыванию цены? (y/n): ").strip()
            is_desc: bool = ans.lower() == "y"
            sorted_items = sort_items_by_price(items, descending=is_desc)
            show_items_detailed(sorted_items, categories)
        elif choice == "9":
            handle_delete_item(items)
        elif choice == "10":
            handle_delete_collection(collections, items)
        elif choice == "11":
            handle_delete_user(users, collections, items)
        elif choice == "0":
            print("Работа завершена.")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
