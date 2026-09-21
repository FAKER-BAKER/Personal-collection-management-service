from typing import Any


def add_user(
    users: list[dict[str, Any]],
    username: str,
    email: str
) -> dict[str, Any]:
    """Регистрирует нового пользователя."""
    new_id = max([u["id"] for u in users], default=0) + 1
    user = {"id": new_id, "username": username, "email": email}
    users.append(user)
    return user


def find_user_by_id(
    users: list[dict[str, Any]],
    user_id: int
) -> dict[str, Any] | None:
    """Ищет пользователя по ID."""
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def find_user_by_username(
    users: list[dict[str, Any]],
    username: str
) -> dict[str, Any] | None:
    """Ищет пользователя по имени."""
    for user in users:
        if user["username"].lower() == username.lower():
            return user
    return None


def delete_user(users: list[dict[str, Any]], user_id: int) -> bool:
    """Удаляет пользователя по ID."""
    for idx, user in enumerate(users):
        if user["id"] == user_id:
            del users[idx]
            return True
    return False
