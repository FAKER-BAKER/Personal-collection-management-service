import json
import os
from typing import Any
from essence.categories import Category
from essence.collections import Collection
from essence.items import Item
from essence.users import User


def load_json_raw(filepath: str) -> list[dict[str, Any]]:
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_json_raw(filepath: str, data: list[dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_users(filepath: str) -> list[User]:
    raw = load_json_raw(filepath)
    return [User.from_data(item) for item in raw]


def save_users(filepath: str, users: list[User]) -> None:
    save_json_raw(filepath, [u.to_dict() for u in users])


def load_categories(filepath: str) -> list[Category]:
    raw = load_json_raw(filepath)
    return [Category.from_data(item) for item in raw]


def save_categories(filepath: str, categories: list[Category]) -> None:
    save_json_raw(filepath, [c.to_dict() for c in categories])


def load_collections(
    filepath: str,
    users: list[User],
) -> list[Collection]:
    raw = load_json_raw(filepath)
    user_map = {u.id: u for u in users}
    collections: list[Collection] = []
    for item in raw:
        user = user_map.get(int(item["user_id"]))
        if user:
            col = Collection(
                collection_id=int(item["id"]),
                user=user,
                name=str(item["name"]),
                description=str(item.get("description", "")),
            )
            collections.append(col)
    return collections


def save_collections(
    filepath: str,
    collections: list[Collection],
) -> None:
    save_json_raw(filepath, [c.to_dict() for c in collections])


def load_items(
    filepath: str,
    collections: list[Collection],
    categories: list[Category],
) -> list[Item]:
    raw = load_json_raw(filepath)
    col_map = {c.id: c for c in collections}
    cat_map = {c.id: c for c in categories}
    items: list[Item] = []
    for data in raw:
        col = col_map.get(int(data["collection_id"]))
        cat = cat_map.get(int(data["category_id"]))
        if col and cat:
            it = Item(
                item_id=int(data["id"]),
                collection=col,
                category=cat,
                name=str(data["name"]),
                year=int(data["year"]),
                condition=str(data["condition"]),
                price=float(data["price"]),
            )
            items.append(it)
    return items


def save_items(filepath: str, items: list[Item]) -> None:
    save_json_raw(filepath, [i.to_dict() for i in items])
