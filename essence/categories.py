from typing import Any


def add_category(
    categories: list[dict[str, Any]],
    name: str,
    description: str
) -> dict[str, Any]:
    """Добавляет категорию предметов."""
    new_id = max([c["id"] for c in categories], default=0) + 1
    category = {"id": new_id, "name": name, "description": description}
    categories.append(category)
    return category


def find_category_by_id(
    categories: list[dict[str, Any]],
    category_id: int
) -> dict[str, Any] | None:
    """Ищет категорию по ID."""
    for cat in categories:
        if cat["id"] == category_id:
            return cat
    return None


def search_categories(
    categories: list[dict[str, Any]],
    query: str
) -> list[dict[str, Any]]:
    """Поиск категорий по подстроке названия."""
    q = query.lower()
    return [c for c in categories if q in c["name"].lower()]


def delete_category(
    categories: list[dict[str, Any]],
    category_id: int
) -> bool:
    """Удаляет категорию."""
    for idx, cat in enumerate(categories):
        if cat["id"] == category_id:
            del categories[idx]
            return True
    return False
