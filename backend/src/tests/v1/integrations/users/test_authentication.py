import freezegun
import pytest
from django.conf import settings
from django.test import Client
from django.utils.timezone import now
from jwt import decode
from ninja.responses import Response

from api.models import IssuedToken, User
from tests.conftest import post, unauthorized_error
from tests.v1.integrations.conftest import USER_PASSWORD
from tests.v1.integrations.users.conftest import USERS, access_payload, refresh_payload

AUTHENTICATE = USERS + "/authenticate"


def authenticate(client: Client, email: str, password: str) -> Response:
    return post(client, AUTHENTICATE, body={"email": email, "password": password})


def decode_payload(token: str) -> dict:
    return decode(token, settings.SECRET_KEY, "HS256")


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate(client: Client, user: User) -> None:
    response = authenticate(client, user.email, USER_PASSWORD)

    assert_success(response, user)


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate__where_entered_not_existed_email(client: Client, user: User) -> None:
    _test_authenticate_with_bad_credentials(client, user, email="bad_email@unknown.dog")


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate__where_entered_wrong_password(client: Client, user: User) -> None:
    _test_authenticate_with_bad_credentials(client, user, password="bad password")


def _test_authenticate_with_bad_credentials(
    client: Client, user: User, email: str = None, password: str = None
) -> None:
    response = authenticate(client, email or user.email, password or USER_PASSWORD)

    assert response.status_code == 401
    assert response.json() == unauthorized_error()
    assert not IssuedToken.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate__where_refresh_token_has_created(client: Client, user: User) -> None:
    token = IssuedToken.objects.create(value="token_value", owner=user)
    assert token.revoked is False

    response = authenticate(client, user.email, USER_PASSWORD)

    assert_success(response, user)
    token.refresh_from_db()
    assert token.revoked is True


def assert_success(response: Response, user: User) -> None:
    assert response.status_code == 200
    body = response.json()
    assert list(body.keys()) == ["access_token"]
    assert decode_payload(body["access_token"]) == access_payload(user)

    refresh = response.cookies[settings.REFRESH_TOKEN_COOKIE].value
    assert decode_payload(refresh) == refresh_payload(user)
    assert IssuedToken.objects.filter(value=refresh, owner=user, revoked=False).exists()
