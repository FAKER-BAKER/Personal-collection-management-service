from typing import Any, Optional
from essence.users import User


class Collection:
    """Коллекция, принадлежащая пользователю."""

    def __init__(
        self,
        collection_id: int,
        user: User,
        name: str,
        description: str = "",
    ) -> None:
        self.id = collection_id
        self.user = user
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return (
            f"Коллекция [{self.id}] «{self.name}» "
            f"(Владелец: {self.user.username})"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user.id,
            "name": self.name,
            "description": self.description,
        }


def add_collection(
    collections: list[Collection],
    user: User,
    name: str,
    description: str = "",
) -> Collection:
    new_id = max((c.id for c in collections), default=0) + 1
    col = Collection(new_id, user, name, description)
    collections.append(col)
    return col


def find_collection_by_id(
    collections: list[Collection],
    collection_id: int,
) -> Optional[Collection]:
    for col in collections:
        if col.id == collection_id:
            return col
    return None


def get_user_collections(
    collections: list[Collection],
    user_id: int,
) -> list[Collection]:
    return [c for c in collections if c.user.id == user_id]


def delete_collection(
    collections: list[Collection],
    collection_id: int,
) -> bool:
    col = find_collection_by_id(collections, collection_id)
    if col:
        collections.remove(col)
        return True
    return False
