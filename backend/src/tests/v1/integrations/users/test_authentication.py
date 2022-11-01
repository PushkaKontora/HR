import freezegun
import pytest
from django.conf import settings
from django.db.models import Q
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import IssuedToken, User
from tests.v1.conftest import USER_PASSWORD
from tests.v1.integrations.conftest import post, unauthorized
from tests.v1.integrations.users.conftest import USERS, access_payload, decode_payload, refresh_payload

AUTHENTICATE = USERS + "/authenticate"


def authenticate(client: Client, email: str, password: str) -> Response:
    return post(client, AUTHENTICATE, body={"email": email, "password": password})


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate(client: Client, user_with_password: User) -> None:
    response = authenticate(client, user_with_password.email, USER_PASSWORD)

    assert_success_with_tokens(response, user_with_password)


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate__when_not_existed_email_was_entered(client: Client, user_with_password: User) -> None:
    _test_authenticate_with_bad_credentials(client, user_with_password, email="bad_email@unknown.dog")


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate__when_wrong_password_was_entered(client: Client, user_with_password: User) -> None:
    _test_authenticate_with_bad_credentials(client, user_with_password, password="bad password")


def _test_authenticate_with_bad_credentials(
    client: Client, user: User, email: str = None, password: str = None
) -> None:
    response = authenticate(client, email or user.email, password or USER_PASSWORD)

    assert response.status_code == 401
    assert response.json() == unauthorized()
    assert not IssuedToken.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_authenticate__when_refresh_token_existed(client: Client, user_with_password: User) -> None:
    token = IssuedToken.objects.create(value="token_value", owner=user_with_password)
    assert token.revoked is False

    response = authenticate(client, user_with_password.email, USER_PASSWORD)

    assert_success_with_tokens(response, user_with_password)
    token.refresh_from_db()
    assert token.revoked is True


def assert_success_with_tokens(response: Response, user: User) -> None:
    assert response.status_code == 200
    body = response.json()
    assert list(body.keys()) == ["access_token"]
    assert decode_payload(body["access_token"]) == access_payload(user)

    refresh = response.cookies[settings.REFRESH_TOKEN_COOKIE].value
    assert decode_payload(refresh) == refresh_payload(user)
    assert IssuedToken.objects.filter(value=refresh, owner=user, revoked=False).exists()
    assert not IssuedToken.objects.filter(~Q(value=refresh) & Q(revoked=False)).exists()
