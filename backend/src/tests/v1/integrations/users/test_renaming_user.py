import pytest
from django.test import Client
from ninja.responses import Response

from api.models import User
from tests.v1.integrations.conftest import forbidden, not_found, patch, success
from tests.v1.integrations.users.conftest import USER

RENAME = USER + "/rename"


def rename(client: Client, user_id: int, token: str, surname: str, name: str, patronymic: str) -> Response:
    return patch(
        client, RENAME.format(user_id=user_id), token, {"surname": surname, "name": name, "patronymic": patronymic}
    )


@pytest.mark.integration
@pytest.mark.django_db
def test_rename_user(
    client: Client, user: User, user_token: str, surname="Dykov", name="Lima", patronymic="Unknown"
) -> None:
    assert user.surname != surname
    assert user.name != name
    assert user.patronymic != patronymic

    response = rename(client, user.id, user_token, surname, name, patronymic)

    assert response.status_code == 200
    assert response.json() == success()

    user.refresh_from_db()
    assert user.surname == surname
    assert user.name == name
    assert user.patronymic == patronymic


@pytest.mark.integration
@pytest.mark.django_db
def test_rename_user__authenticated_user_try_it_with_another(
    client: Client, user: User, another_user: User, user_token: str
) -> None:
    surname, name, patronymic = user.surname, user.name, user.patronymic

    response = rename(client, another_user.id, user_token, "a", "b", "c")

    assert response.status_code == 403
    assert response.json() == forbidden()

    user.refresh_from_db()
    assert user.surname == surname
    assert user.name == name
    assert user.patronymic == patronymic


@pytest.mark.integration
@pytest.mark.django_db
def test_rename_unknown_user(client: Client, user: User, user_token: str) -> None:
    response = rename(client, 0, user_token, "a", "b", "c")

    assert response.status_code == 404
    assert response.json() == not_found()

    assert User.objects.get(pk=user.pk) == user
