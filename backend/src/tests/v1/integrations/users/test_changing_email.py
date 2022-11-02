import pytest
from django.test import Client
from ninja.responses import Response

from api.models import User
from tests.v1.integrations.conftest import error_422, forbidden, not_found, patch, success
from tests.v1.integrations.users.conftest import USER

CHANGE = USER + "/email"

EMAIL_REGISTERED_ERROR = error_422(11, "The email is already registered")


def change(client: Client, user_id: int, token: str, email: str) -> Response:
    return patch(client, CHANGE.format(user_id=user_id), token, {"email": email})


@pytest.mark.integration
@pytest.mark.django_db
def test_changing_email(client: Client, user: User, user_token: str, new_email="lima.dykov@gmail.com") -> None:
    assert user.email != new_email

    response = change(client, user.id, user_token, new_email)

    assert response.status_code == 200
    assert response.json() == success()

    user.refresh_from_db()
    assert user.email == new_email


@pytest.mark.integration
@pytest.mark.django_db
def test_changing_email__the_email_is_already_registered_by_another_user(
    client: Client, user: User, user_token: str, another_user: User
) -> None:
    assert user.email != another_user.email
    expected_email = user.email

    response = change(client, user.id, user_token, another_user.email)

    assert response.status_code == 422
    assert response.json() == EMAIL_REGISTERED_ERROR

    user.refresh_from_db()
    assert user.email == expected_email


@pytest.mark.integration
@pytest.mark.django_db
def test_changing_email__the_email_is_already_registered_by_self(client: Client, user: User, user_token: str) -> None:
    expected_email = user.email

    response = change(client, user.id, user_token, user.email)

    assert response.status_code == 422
    assert response.json() == EMAIL_REGISTERED_ERROR

    user.refresh_from_db()
    assert user.email == expected_email


@pytest.mark.integration
@pytest.mark.django_db
def test_changing_email__authorized_user_try_it_with_another(
    client: Client, user: User, user_token: str, another_user: User, new_email="lima.dykov@gmail.com"
) -> None:
    assert user.email != new_email
    expected_user_email, expected_another_user_email = user.email, another_user.email

    response = change(client, another_user.id, user_token, new_email)

    assert response.status_code == 403
    assert response.json() == forbidden()

    user.refresh_from_db()
    another_user.refresh_from_db()
    assert user.email == expected_user_email
    assert another_user.email == expected_another_user_email


@pytest.mark.integration
@pytest.mark.django_db
def test_changing_email_of_unknown_user(client: Client, user: User, user_token: str) -> None:
    response = change(client, 0, user_token, "123@123.com")

    assert response.status_code == 404
    assert response.json() == not_found()

    assert User.objects.get(pk=user.pk).email == user.email
