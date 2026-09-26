from typing import Any
from essence.items import (
    add_item,
    check_rarity,
    get_items_by_collection,
    get_total_value,
    sort_items_by_price,
)


def test_add_item_and_collection_link() -> None:
    items: list[dict[str, Any]] = []
    i = add_item(
        items,
        collection_id=10,
        category_id=2,
        name="Рубль",
        year=1900,
        condition="Отл",
        price=5000.0,
    )
    assert len(items) == 1
    assert i["collection_id"] == 10


def test_check_rarity() -> None:
    assert check_rarity(1820) == "Раритет (более 100 лет)"
    assert check_rarity(2025) == "Современный"


def test_get_items_by_collection() -> None:
    items: list[dict[str, Any]] = [
        {"id": 1, "collection_id": 1, "price": 100.0},
        {"id": 2, "collection_id": 2, "price": 200.0}
    ]
    res = get_items_by_collection(items, collection_id=1)
    assert len(res) == 1
    assert res[0]["id"] == 1


def test_sort_and_total_value() -> None:
    items: list[dict[str, Any]] = [
        {"id": 1, "price": 500.0},
        {"id": 2, "price": 1500.0}
    ]
    sorted_res = sort_items_by_price(items, descending=True)
    assert sorted_res[0]["price"] == 1500.0
    assert get_total_value(items) == 2000.0
