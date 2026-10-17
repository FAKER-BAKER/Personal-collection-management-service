from essence.categories import (
    Category,
    add_category,
    find_category_by_id,
)
from essence.collections import (
    Collection,
    add_collection,
    delete_collection,
    find_collection_by_id,
)
from essence.items import (
    Item,
    add_item,
    delete_item,
    get_total_value,
    sort_items_by_price,
)
from essence.users import User, add_user, delete_user, find_user_by_id
from storage import (
    load_categories,
    load_collections,
    load_items,
    load_users,
    save_categories,
    save_collections,
    save_items,
    save_users,
)
from utils import input_float, input_int, input_non_empty

FILES = {
    "users": "data/users.json",
    "categories": "data/categories.json",
    "collections": "data/collections.json",
    "items": "data/items.json",
}


def show_summary(
    users: list[User],
    categories: list[Category],
    collections: list[Collection],
    items: list[Item],
) -> None:
    print("\n--- Общая статистика системы (ООП) ---")
    print(f"Пользователей: {len(users)}")
    print(f"Категорий: {len(categories)}")
    print(f"Коллекций: {len(collections)}")
    print(f"Предметов всего: {len(items)}")
    val = get_total_value(items)
    print(f"Общая оценочная стоимость: {val:,.2f} руб.")


def show_items_detailed(items: list[Item]) -> None:
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
        row = (
            f"{i.id:<4} | {i.name[:20]:<22} | {i.category.name[:12]:<14} | "
            f"{i.year:<6} | {i.price:<10.2f} | {i.check_rarity()}"
        )
        print(row)
    print(sep)


def handle_delete_item(items: list[Item]) -> None:
    if not items:
        print("Список предметов пуст.")
        return
    item_id = input_int("Введите ID предмета для удаления: ", min_val=1)
    if delete_item(items, item_id):
        save_items(FILES["items"], items)
        print(f"Предмет с ID {item_id} успешно удален.")
    else:
        print(f"Предмет с ID {item_id} не найден.")


def handle_delete_collection(
    collections: list[Collection],
    items: list[Item],
) -> None:
    if not collections:
        print("Список коллекций пуст.")
        return
    col_id = input_int("Введите ID коллекции для удаления: ", min_val=1)
    if delete_collection(collections, col_id):
        save_collections(FILES["collections"], collections)
        items[:] = [i for i in items if i.collection.id != col_id]
        save_items(FILES["items"], items)
        print(f"Коллекция ID {col_id} и связанные предметы удалены.")
    else:
        print(f"Коллекция с ID {col_id} не найдена.")


def handle_delete_user(
    users: list[User],
    collections: list[Collection],
    items: list[Item],
) -> None:
    if not users:
        print("Список пользователей пуст.")
        return
    u_id = input_int("Введите ID пользователя для удаления: ", min_val=1)
    user_col_ids = {c.id for c in collections if c.user.id == u_id}

    if delete_user(users, u_id):
        save_users(FILES["users"], users)
        collections[:] = [c for c in collections if c.id not in user_col_ids]
        save_collections(FILES["collections"], collections)
        items[:] = [i for i in items if i.collection.id not in user_col_ids]
        save_items(FILES["items"], items)
        print(f"Пользователь ID {u_id} и все его данные удалены.")
    else:
        print(f"Пользователь с ID {u_id} не найден.")


def main() -> None:
    users = load_users(FILES["users"])
    categories = load_categories(FILES["categories"])
    collections = load_collections(FILES["collections"], users)
    items = load_items(FILES["items"], collections, categories)

    while True:
        print("\n=== Сервис управления коллекциями (ПР3: ООП) ===")
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
                print(u)
        elif choice == "3":
            uname = input_non_empty("Имя пользователя: ")
            email = input_non_empty("Email: ")
            u = add_user(users, uname, email)
            save_users(FILES["users"], users)
            print(f"Создан: {u}")
        elif choice == "4":
            print("\nКатегории:")
            for c in categories:
                print(c)
        elif choice == "5":
            name = input_non_empty("Название категории: ")
            desc = input_non_empty("Описание: ")
            cat = add_category(categories, name, desc)
            save_categories(FILES["categories"], categories)
            print(f"Создана: {cat}")
        elif choice == "6":
            if not users:
                print("Сначала создайте пользователя!")
                continue
            u_id = input_int("Введите ID владельца: ", min_val=1)
            owner = find_user_by_id(users, u_id)
            if not owner:
                print("Пользователь не найден.")
                continue
            c_name = input_non_empty("Название коллекции: ")
            c_desc = input_non_empty("Описание коллекции: ")
            col = add_collection(collections, owner, c_name, c_desc)
            save_collections(FILES["collections"], collections)
            print(f"Создана: {col}")
        elif choice == "7":
            if not collections or not categories:
                print("Сначала создайте коллекцию и категорию!")
                continue
            col_id = input_int("ID коллекции: ", min_val=1)
            target_col = find_collection_by_id(collections, col_id)
            if not target_col:
                print("Коллекция не найдена.")
                continue
            cat_id = input_int("ID категории: ", min_val=1)
            target_cat = find_category_by_id(categories, cat_id)
            if not target_cat:
                print("Категория не найдена.")
                continue
            name = input_non_empty("Название предмета: ")
            year = input_int("Год выпуска: ", min_val=1, max_val=2026)
            cond = input_non_empty("Состояние: ")
            price = input_float("Стоимость (руб.): ", min_val=0.0)
            it = add_item(
                items, target_col, target_cat, name, year, cond, price
            )
            save_items(FILES["items"], items)
            print(f"Добавлен: {it}")
        elif choice == "8":
            ans: str = input("Сортировать по убыванию цены? (y/n): ").strip()
            is_desc: bool = ans.lower() == "y"
            sorted_items = sort_items_by_price(items, descending=is_desc)
            show_items_detailed(sorted_items)
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
