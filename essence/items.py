from typing import Any, Optional
from essence.categories import Category
from essence.collections import Collection


class Item:
    """Предмет коллекции."""

    def __init__(
        self,
        item_id: int,
        collection: Collection,
        category: Category,
        name: str,
        year: int,
        condition: str,
        price: float,
    ) -> None:
        self.id = item_id
        self.collection = collection
        self.category = category
        self.name = name
        self.year = year
        self.condition = condition
        self.price = price

    def check_rarity(self) -> str:
        """Метод объекта: определение редкости предмета по году выпуска."""
        if self.year < 1950:
            return "Раритет"
        if self.year < 1990:
            return "Винтаж"
        return "Современный"

    def is_expensive(self, threshold: float = 10000.0) -> bool:
        """Метод объекта: проверка высокой стоимости предмета."""
        return self.price >= threshold

    def __str__(self) -> str:
        return (
            f"Предмет [{self.id}] «{self.name}» ({self.year} г., "
            f"{self.check_rarity()}) — {self.price:,.2f} руб."
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "collection_id": self.collection.id,
            "category_id": self.category.id,
            "name": self.name,
            "year": self.year,
            "condition": self.condition,
            "price": self.price,
        }


def add_item(
    items: list[Item],
    collection: Collection,
    category: Category,
    name: str,
    year: int,
    condition: str,
    price: float,
) -> Item:
    new_id = max((i.id for i in items), default=0) + 1
    item = Item(new_id, collection, category, name, year, condition, price)
    items.append(item)
    return item


def find_item_by_id(items: list[Item], item_id: int) -> Optional[Item]:
    for it in items:
        if it.id == item_id:
            return it
    return None


def get_items_by_collection(
    items: list[Item],
    collection_id: int,
) -> list[Item]:
    return [i for i in items if i.collection.id == collection_id]


def get_total_value(items: list[Item]) -> float:
    return sum(i.price for i in items)


def sort_items_by_price(
    items: list[Item],
    descending: bool = True,
) -> list[Item]:
    return sorted(items, key=lambda x: x.price, reverse=descending)


def delete_item(items: list[Item], item_id: int) -> bool:
    item = find_item_by_id(items, item_id)
    if item:
        items.remove(item)
        return True
    return False
