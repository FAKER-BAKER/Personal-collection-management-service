from essence.categories import (
    Category,
    add_category,
    delete_category,
    find_category_by_id,
)


def test_category_creation() -> None:
    cat = Category(1, "Монеты", "Старинные монеты")
    assert cat.id == 1
    assert cat.name == "Монеты"
    assert "Монеты" in str(cat)


def test_add_and_delete_category() -> None:
    cats: list[Category] = []
    cat = add_category(cats, "Марки", "Почтовые марки")
    assert len(cats) == 1
    assert find_category_by_id(cats, cat.id) is cat
    assert delete_category(cats, cat.id) is True
    assert len(cats) == 0
