from essence.collections import (
    Collection,
    add_collection,
    delete_collection,
    get_user_collections,
)
from essence.users import User


def test_collection_creation_and_links() -> None:
    user = User(1, "alex", "alex@mail.ru")
    col = Collection(1, user, "Нумизматика", "Моя коллекция")
    assert col.user is user
    assert col.user.username == "alex"
    assert "Нумизматика" in str(col)


def test_user_collections_filtering() -> None:
    u1 = User(1, "u1", "u1@mail.ru")
    u2 = User(2, "u2", "u2@mail.ru")
    cols: list[Collection] = []
    add_collection(cols, u1, "Коллекция 1")
    add_collection(cols, u2, "Коллекция 2")
    add_collection(cols, u1, "Коллекция 3")

    user1_cols = get_user_collections(cols, 1)
    assert len(user1_cols) == 2
    assert delete_collection(cols, user1_cols[0].id) is True
    assert len(cols) == 2
