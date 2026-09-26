from datetime import date
from typing import Any


def check_rarity(year: int) -> str:
    """Определяет редкость по году выпуска (из ПР1)."""
    current_year = date.today().year
    age = current_year - year
    if age >= 100:
        return "Раритет (более 100 лет)"
    elif age >= 50:
        return "Редкий (более 50 лет)"
    elif age >= 20:
        return "Старинный (более 20 лет)"
    return "Современный"


def add_item(
    items: list[dict[str, Any]],
    collection_id: int,
    category_id: int,
    name: str,
    year: int,
    condition: str,
    price: float
) -> dict[str, Any]:
    """Добавляет предмет в коллекцию."""
    new_id = max([i["id"] for i in items], default=0) + 1
    item = {
        "id": new_id,
        "collection_id": collection_id,
        "category_id": category_id,
        "name": name,
        "year": year,
        "condition": condition,
        "price": price
    }
    items.append(item)
    return item


def get_items_by_collection(
    items: list[dict[str, Any]],
    collection_id: int
) -> list[dict[str, Any]]:
    """Возвращает предметы конкретной коллекции."""
    return [i for i in items if i["collection_id"] == collection_id]


def sort_items_by_price(
    items: list[dict[str, Any]],
    descending: bool = False
) -> list[dict[str, Any]]:
    """Сортировка предметов через lambda."""
    return sorted(items, key=lambda x: x["price"], reverse=descending)


def get_total_value(items: list[dict[str, Any]]) -> float:
    """Суммарная стоимость предметов (из ПР1)."""
    return sum(i["price"] for i in items)


def delete_item(items: list[dict[str, Any]], item_id: int) -> bool:
    """Удаляет предмет."""
    for idx, item in enumerate(items):
        if item["id"] == item_id:
            del items[idx]
            return True
    return False
