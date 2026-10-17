from essence.users import User, add_user, delete_user, find_user_by_id


def test_user_creation() -> None:
    user = User(1, "alex", "alex@mail.ru")
    assert user.id == 1
    assert user.username == "alex"
    assert "alex" in str(user)


def test_user_from_data() -> None:
    data = {"id": 2, "username": "bob", "email": "bob@mail.ru"}
    user = User.from_data(data)
    assert user.id == 2
    assert user.username == "bob"


def test_add_and_find_user() -> None:
    users: list[User] = []
    user = add_user(users, "clara", "clara@mail.ru")
    assert len(users) == 1
    assert find_user_by_id(users, user.id) is user
    assert find_user_by_id(users, 999) is None


def test_delete_user() -> None:
    users: list[User] = []
    user = add_user(users, "dan", "dan@mail.ru")
    assert delete_user(users, user.id) is True
    assert len(users) == 0
    assert delete_user(users, 999) is False
