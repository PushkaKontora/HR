from datetime import timedelta
from time import sleep

import freezegun
import pytest
from django.conf import settings
from django.http import SimpleCookie

from django.test import Client
from django.utils.timezone import now
from jwt import encode
from ninja.responses import Response

from api.models import IssuedToken, User
from tests.conftest import post, message
from tests.v1.integrations.users.conftest import USERS, refresh_payload, encode_payload
from tests.v1.integrations.users.test_authentication import assert_success_with_tokens

REFRESH = USERS + "/refresh-tokens"

INVALID_SIGNATURE = "Invalid signature"
INVALID_PAYLOAD = "Invalid payload"
UNKNOWN_USER_ID = "Unknown user id"
TOKEN_IS_EXPIRED = "The token is expired"
TOKEN_IS_REVOKED = "The token is revoked"
REFRESH_TOKEN_IS_NOT_IN_COOKIES = "Refresh token is not in cookies"


def refresh(client: Client, refresh_token: str = None) -> Response:
    if refresh_token is not None:
        client.cookies = SimpleCookie({settings.REFRESH_TOKEN_COOKIE: refresh_token})

    return post(client, REFRESH)


@pytest.mark.integration
@pytest.mark.django_db
def test_refresh(client: Client, user: User) -> None:
    token = IssuedToken.objects.create(owner=user, value=encode_payload(refresh_payload(user)), revoked=False)

    with freezegun.freeze_time(now() - timedelta(days=10)):
        response = refresh(client, token.value)

        assert_success_with_tokens(response, user)
        token.refresh_from_db()
        assert token.revoked


@pytest.mark.integration
@pytest.mark.django_db
def test_refresh__when_token_is_not_in_cookies(client: Client, user: User) -> None:
    token = IssuedToken.objects.create(owner=user, value="123", revoked=False)

    response = refresh(client)

    assert response.status_code == 400
    assert response.json() == message(REFRESH_TOKEN_IS_NOT_IN_COOKIES)

    token.refresh_from_db()
    assert not token.revoked
    assert IssuedToken.objects.filter(owner=user).count() == 1


@pytest.mark.integration
@pytest.mark.django_db
def test_refresh__if_token_was_created_with_wrong_secret_key(client: Client, user: User) -> None:
    token = encode(refresh_payload(user), "wrong secret key")

    response = refresh(client, token)

    assert_invalid_signature(response, user)


@pytest.mark.integration
@pytest.mark.django_db
def test_refresh__if_token_has_wrong_payload(client: Client, user: User) -> None:
    token = encode({"user_id": 1}, settings.SECRET_KEY)

    response = refresh(client, token)

    assert_invalid_payload(response, user)


@pytest.mark.integration
@pytest.mark.django_db
def test_refresh__when_some_char_was_removed_from_token(client: Client, user: User) -> None:
    token = encode_payload(refresh_payload(user))[1:]

    response = refresh(client, token)

    assert_invalid_signature(response, user)


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize("delta", [
    timedelta(0),
    timedelta(seconds=1),
    timedelta(seconds=10),
    timedelta(days=30),
])
@freezegun.freeze_time(now())
def test_refresh__when_token_is_expired(client: Client, user: User, delta: timedelta) -> None:
    payload = refresh_payload(user)
    assert "exp" in payload
    payload["exp"] = int((now() + delta).timestamp())

    response = refresh(client, encode_payload(payload))

    assert response.status_code == 400
    assert response.json() == message(TOKEN_IS_EXPIRED)
    assert not IssuedToken.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_refresh__when_token_is_revoked(client: Client, user: User) -> None:
    alive = IssuedToken.objects.create(owner=user, value=encode_payload(refresh_payload(user)), revoked=False)
    sleep(1)
    revoked = IssuedToken.objects.create(owner=user, value=encode_payload(refresh_payload(user)), revoked=True)

    response = refresh(client, revoked.value)

    assert response.status_code == 400
    assert response.json() == message(TOKEN_IS_REVOKED)
    assert not IssuedToken.objects.filter(owner=user, revoked=False).exists()


def assert_invalid_signature(response: Response, user: User) -> None:
    assert response.status_code == 400
    assert response.json() == message(INVALID_SIGNATURE)
    assert not IssuedToken.objects.filter(owner=user).exists()


def assert_invalid_payload(response: Response, user: User) -> None:
    assert response.status_code == 400
    assert response.json() == message(INVALID_PAYLOAD)
    assert not IssuedToken.objects.filter(owner=user).exists()
