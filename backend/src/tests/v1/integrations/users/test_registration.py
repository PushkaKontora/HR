import pytest
from bcrypt import checkpw
from django.db.models import Q
from django.test import Client
from ninja.responses import Response

from api.models import Permissions, Resume, User
from tests.conftest import get_422_error, post
from tests.v1.integrations.users.conftest import USERS


def registrate(client: Client, body: dict) -> Response:
    return post(client, USERS, body=body)


@pytest.mark.integration
@pytest.mark.django_db
def test_register_user(client: Client) -> None:
    body = {
        "email": "address@gmail.com",
        "password": "очень secret password",
        "surname": "Ivanov",
        "name": "Pety",
        "patronymic": "Sidorov",
    }
    response = registrate(client, body)

    assert response.status_code == 200

    user = User.objects.get(surname=body["surname"], name=body["name"], patronymic=body["patronymic"])

    assert user.email == body["email"]
    assert checkpw(body["password"].encode(), user.password.value.encode()) is True

    assert user.permission == Permissions.USER
    assert bool(user.photo) is False
    assert not Resume.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_register_user__where_email_has_already_taken(client: Client) -> None:
    body = {
        "email": "address@gmail.com",
        "password": "очень secret password",
        "surname": "Ivanov",
        "name": "Pety",
        "patronymic": "Sidorov",
    }

    user = User.objects.create(email=body["email"], surname="A", name="B", patronymic="C")

    response = registrate(client, body)

    assert response.status_code == 422
    assert response.json() == get_422_error(1, "The email has already registered")

    assert User.objects.filter(email=user.email).count() == 1
    assert not User.objects.filter(surname=body["surname"], name=body["name"], patronymic=body["patronymic"]).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_register_user__where_full_name_has_already_created(client: Client, another_email="another@mail.ru") -> None:
    body = {
        "email": "address@gmail.com",
        "password": "очень secret password",
        "surname": "Ivanov",
        "name": "Pety",
        "patronymic": "Sidorov",
    }
    response = registrate(client, body)

    assert response.status_code == 200

    user = User.objects.create(
        email=another_email, surname=body["surname"], name=body["name"], patronymic=body["patronymic"]
    )

    assert User.objects.filter(surname=body["surname"], name=body["name"], patronymic=body["patronymic"]).count() == 2
    assert User.objects.filter(~Q(pk=user.pk)).get().email == body["email"]
