from datetime import timedelta
from unittest.mock import MagicMock

import freezegun
import pytest
from django.conf import settings
from django.utils.timezone import now
from jwt import encode

from api.internal.errors import UnauthorizedError
from api.internal.v1.users.api import UsersContainer
from api.models import User
from tests.v1.integrations.users.conftest import access_payload, encode_payload

INVALID_SIGNATURE_OR_PAYLOAD = "Invalid signature or payload"
TOKEN_IS_EXPIRED = "The token is expired"
UNKNOWN_USER_ID = "Unknown user id"

jwt = UsersContainer().auth()


@pytest.mark.module
@pytest.mark.django_db
def test_jwt_auth(user: User) -> None:
    request = MagicMock()
    token = encode_payload(access_payload(user))

    assert jwt.authenticate(request, token) == token
    assert request.user == user


@pytest.mark.module
@pytest.mark.django_db
def test_jwt_auth__if_token_was_created_with_wrong_secret_key(user: User) -> None:
    request = MagicMock()
    token = encode(access_payload(user), "wrong secret key")

    with pytest.raises(UnauthorizedError, match=INVALID_SIGNATURE_OR_PAYLOAD):
        jwt.authenticate(request, token)

    assert request.user is None


@pytest.mark.module
@pytest.mark.django_db
def test_jwt_auth__if_token_has_wrong_payload(user: User) -> None:
    request = MagicMock()
    token = encode({"user_id": 1}, settings.SECRET_KEY)

    with pytest.raises(UnauthorizedError, match=INVALID_SIGNATURE_OR_PAYLOAD):
        jwt.authenticate(request, token)

    assert request.user is None


@pytest.mark.module
@pytest.mark.django_db
def test_jwt_auth__when_some_char_was_removed_from_token(user: User) -> None:
    request = MagicMock()
    token = encode_payload(access_payload(user))[1:]

    with pytest.raises(UnauthorizedError, match=INVALID_SIGNATURE_OR_PAYLOAD):
        jwt.authenticate(request, token)

    assert request.user is None


@pytest.mark.module
@pytest.mark.django_db
@pytest.mark.parametrize("name", ["unknown", "refresh"])
def test_jwt_auth__when_wrong_type_is_in_payload(user: User, name: str) -> None:
    request = MagicMock()
    payload = access_payload(user)
    assert "type" in payload

    payload["type"] = name

    with pytest.raises(UnauthorizedError, match=INVALID_SIGNATURE_OR_PAYLOAD):
        jwt.authenticate(request, encode_payload(payload))

    assert request.user is None


@pytest.mark.module
@pytest.mark.django_db
@pytest.mark.parametrize(
    "delta",
    [
        timedelta(0),
        timedelta(seconds=1),
        timedelta(seconds=10),
        timedelta(days=30),
    ],
)
@freezegun.freeze_time(now())
def test_jwt_auth__when_token_is_expired(user: User, delta: timedelta) -> None:
    request = MagicMock()
    payload = access_payload(user)
    assert "expires_in" in payload

    payload["expires_in"] = int((now() - delta).timestamp())

    with pytest.raises(UnauthorizedError, match=TOKEN_IS_EXPIRED):
        jwt.authenticate(request, encode_payload(payload))

    assert request.user is None


@pytest.mark.module
@pytest.mark.django_db
def test_jwt_auth__if_user_id_is_unknown(user: User) -> None:
    request = MagicMock()
    payload = access_payload(user)
    assert "user_id" in payload
    payload["user_id"] = 0

    with pytest.raises(UnauthorizedError, match=UNKNOWN_USER_ID):
        jwt.authenticate(request, encode_payload(payload))

    assert request.user is None
