from typing import Any, Optional


class User:
    """Пользователь системы."""

    def __init__(self, user_id: int, username: str, email: str) -> None:
        self.id = user_id
        self.username = username
        self.email = email

    def __str__(self) -> str:
        return f"Пользователь [{self.id}] {self.username} ({self.email})"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "User":
        return cls(
            user_id=int(data["id"]),
            username=str(data["username"]),
            email=str(data["email"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


def add_user(users: list[User], username: str, email: str) -> User:
    new_id = max((u.id for u in users), default=0) + 1
    user = User(new_id, username, email)
    users.append(user)
    return user


def find_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    for user in users:
        if user.id == user_id:
            return user
    return None


def delete_user(users: list[User], user_id: int) -> bool:
    user = find_user_by_id(users, user_id)
    if user:
        users.remove(user)
        return True
    return False
