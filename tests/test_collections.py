from typing import Any
from essence.collections import (
    add_collection,
    delete_collection,
    find_collection_by_id,
    get_user_collections,
)


def test_add_collection() -> None:
    cols: list[dict[str, Any]] = []
    c = add_collection(cols, 1, "Монеты", "Мои монеты")
    assert len(cols) == 1
    assert c["user_id"] == 1


def test_get_user_collections() -> None:
    cols: list[dict[str, Any]] = [
        {"id": 1, "user_id": 1, "name": "Коллекция 1"},
        {"id": 2, "user_id": 2, "name": "Коллекция 2"},
        {"id": 3, "user_id": 1, "name": "Коллекция 3"}
    ]
    user1_cols = get_user_collections(cols, user_id=1)
    assert len(user1_cols) == 2


def test_find_collection_by_id() -> None:
    cols: list[dict[str, Any]] = [{"id": 5, "user_id": 1, "name": "Винил"}]
    assert find_collection_by_id(cols, 5) is not None
    assert find_collection_by_id(cols, 1) is None


def test_delete_collection() -> None:
    cols: list[dict[str, Any]] = [{"id": 1, "user_id": 1, "name": "A"}]
    assert delete_collection(cols, 1) is True
    assert len(cols) == 0
