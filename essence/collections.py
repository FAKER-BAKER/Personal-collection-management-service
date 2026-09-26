from typing import Any


def add_collection(
    collections: list[dict[str, Any]],
    user_id: int,
    name: str,
    description: str
) -> dict[str, Any]:
    """Создает коллекцию для конкретного пользователя."""
    new_id = max([c["id"] for c in collections], default=0) + 1
    collection = {
        "id": new_id,
        "user_id": user_id,
        "name": name,
        "description": description
    }
    collections.append(collection)
    return collection


def get_user_collections(
    collections: list[dict[str, Any]],
    user_id: int
) -> list[dict[str, Any]]:
    """Возвращает все коллекции конкретного пользователя."""
    return [c for c in collections if c["user_id"] == user_id]


def find_collection_by_id(
    collections: list[dict[str, Any]],
    col_id: int
) -> dict[str, Any] | None:
    """Ищет коллекцию по ID."""
    for col in collections:
        if col["id"] == col_id:
            return col
    return None


def delete_collection(
    collections: list[dict[str, Any]],
    col_id: int
) -> bool:
    """Удаляет коллекцию."""
    for idx, col in enumerate(collections):
        if col["id"] == col_id:
            del collections[idx]
            return True
    return False
