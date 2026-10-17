from typing import Any, Optional


class Category:
    """Категория предметов коллекции."""

    def __init__(
        self,
        category_id: int,
        name: str,
        description: str = "",
    ) -> None:
        self.id = category_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"Категория [{self.id}] {self.name}: {self.description}"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Category":
        return cls(
            category_id=int(data["id"]),
            name=str(data["name"]),
            description=str(data.get("description", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


def add_category(
    categories: list[Category],
    name: str,
    description: str = "",
) -> Category:
    new_id = max((c.id for c in categories), default=0) + 1
    category = Category(new_id, name, description)
    categories.append(category)
    return category


def find_category_by_id(
    categories: list[Category],
    category_id: int,
) -> Optional[Category]:
    for cat in categories:
        if cat.id == category_id:
            return cat
    return None


def delete_category(categories: list[Category], category_id: int) -> bool:
    cat = find_category_by_id(categories, category_id)
    if cat:
        categories.remove(cat)
        return True
    return False
