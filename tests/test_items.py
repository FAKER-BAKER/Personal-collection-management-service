from essence.categories import Category
from essence.collections import Collection
from essence.items import (
    Item,
    add_item,
    delete_item,
    get_items_by_collection,
    get_total_value,
    sort_items_by_price,
)
from essence.users import User


def test_item_rarity_and_methods() -> None:
    user = User(1, "alex", "alex@mail.ru")
    col = Collection(1, user, "Монеты")
    cat = Category(1, "Золото")
    item_old = Item(1, col, cat, "Рубль 1898", 1898, "Идеальное", 25000.0)
    item_new = Item(2, col, cat, "Юбилейный рубль", 2014, "Отличное", 500.0)

    assert item_old.check_rarity() == "Раритет"
    assert item_new.check_rarity() == "Современный"
    assert item_old.is_expensive(20000.0) is True
    assert item_new.is_expensive(20000.0) is False
    assert item_old.collection.user.username == "alex"


def test_item_operations() -> None:
    user = User(1, "alex", "alex@mail.ru")
    col = Collection(1, user, "Монеты")
    cat = Category(1, "Золото")
    items: list[Item] = []
    i1 = add_item(items, col, cat, "П1", 1920, "Хор", 100.0)
    add_item(items, col, cat, "П2", 2000, "Хор", 300.0)

    assert get_total_value(items) == 400.0
    sorted_items = sort_items_by_price(items, descending=True)
    assert sorted_items[0].price == 300.0

    by_col = get_items_by_collection(items, col.id)
    assert len(by_col) == 2

    assert delete_item(items, i1.id) is True
    assert len(items) == 1
