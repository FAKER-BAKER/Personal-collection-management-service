from typing import Any
from essence.categories import (
    add_category,
    delete_category,
    find_category_by_id,
    search_categories,
)


def test_add_category() -> None:
    cats: list[dict[str, Any]] = []
    c = add_category(cats, "Книги", "Антикварные книги")
    assert len(cats) == 1
    assert c["name"] == "Книги"


def test_find_category_by_id() -> None:
    cats: list[dict[str, Any]] = [{"id": 10, "name": "Монеты", "description": ""}]
    assert find_category_by_id(cats, 10) is not None
    assert find_category_by_id(cats, 99) is None


def test_search_categories() -> None:
    cats: list[dict[str, Any]] = [
        {"id": 1, "name": "Золотые монеты"},
        {"id": 2, "name": "Виниловые пластинки"}
    ]
    res = search_categories(cats, "монет")
    assert len(res) == 1
    assert res[0]["id"] == 1


def test_delete_category() -> None:
    cats: list[dict[str, Any]] = [{"id": 1, "name": "Марки"}]
    assert delete_category(cats, 1) is True
    assert len(cats) == 0
