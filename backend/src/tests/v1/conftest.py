import pytest

from api.internal.v1.users.db.repositories import hash_password
from api.models import Password, User

USER_PASSWORD = "13_очень secret password_37"


@pytest.fixture
def user() -> User:
    return User.objects.create(email="address@gmail.com", surname="Sidorov", name="Ivan", patronymic="Fedorovich")


@pytest.fixture
def user_with_password(user: User) -> User:
    Password.objects.create(owner=user, value=hash_password(USER_PASSWORD))

    return user
