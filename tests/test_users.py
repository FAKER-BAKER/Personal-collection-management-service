from typing import Any
from essence.users import (
    add_user,
    delete_user,
    find_user_by_id,
    find_user_by_username,
)


def test_add_user() -> None:
    users: list[dict[str, Any]] = []
    u = add_user(users, "ivan", "ivan@test.com")
    assert len(users) == 1
    assert u["id"] == 1


def test_find_user_by_id() -> None:
    users: list[dict[str, Any]] = [
        {"id": 1, "username": "ivan", "email": "a@a.com"}
    ]
    found = find_user_by_id(users, 1)
    assert found is not None
    assert found["username"] == "ivan"


def test_find_user_by_username() -> None:
    users: list[dict[str, Any]] = [
        {"id": 1, "username": "ivan", "email": "a@a.com"}
    ]
    assert find_user_by_username(users, "IVAN") is not None
    assert find_user_by_username(users, "petr") is None


def test_delete_user() -> None:
    users: list[dict[str, Any]] = [{"id": 1, "username": "ivan"}]
    assert delete_user(users, 1) is True
    assert len(users) == 0
