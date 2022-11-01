from datetime import timedelta

import freezegun
import pytest
from bcrypt import checkpw
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import User
from tests.v1.conftest import ANOTHER_USER_PASSWORD, USER_PASSWORD
from tests.v1.integrations.conftest import datetime_to_string, error_422, forbidden, patch
from tests.v1.integrations.users.conftest import USER, access_payload, encode_payload

RESET = USER + "/reset-password"

PREVIOUS_PASSWORD_IS_WRONG_RESPONSE = error_422(2, "The previous password does not match with expected")
ONLY_SELF = "Only self"


def reset(client: Client, user_id: int, token: str, prev_password: str, new_password: str) -> Response:
    return patch(
        client, RESET.format(user_id=user_id), token, {"previous_password": prev_password, "new_password": new_password}
    )


def expected_response() -> dict:
    return {"updated_at": datetime_to_string(now())}


@pytest.mark.integration
@pytest.mark.django_db
def test_reset_password(client: Client, user_with_password: User, new_password="new password") -> None:
    password = user_with_password.password

    with freezegun.freeze_time(now() + timedelta(days=10)):
        token = encode_payload(access_payload(user_with_password))

        response = reset(client, user_with_password.id, token, USER_PASSWORD, new_password)
        password.refresh_from_db()

        assert response.status_code == 200
        assert response.json() == expected_response()
        assert checkpw(new_password.encode(), password.value.encode())
        assert password.updated_at == now()


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_reset_password__if_prev_password_is_wrong_for_correct_user_id_in_token(
    client: Client, user_with_password: User, wrong_prev_password="bad password", new_password="new"
) -> None:
    password = user_with_password.password
    expected_updated_at = password.updated_at

    with freezegun.freeze_time(now() + timedelta(days=10)):
        token = encode_payload(access_payload(user_with_password))

        response = reset(client, user_with_password.id, token, wrong_prev_password, new_password)
        password.refresh_from_db()

        assert response.status_code == 422
        assert response.json() == PREVIOUS_PASSWORD_IS_WRONG_RESPONSE
        assert checkpw(USER_PASSWORD.encode(), password.value.encode())
        assert password.updated_at == expected_updated_at


@pytest.mark.integration
@pytest.mark.django_db
def test_reset_password__if_prev_password_is_correct_for_another_user_but_wrong_user_id_in_token(
    client: Client,
    user_with_password: User,
    another_user_with_password: User,
    new_password="new password",
) -> None:
    user_password, another_password = user_with_password.password, another_user_with_password.password
    expected_user_updated_at, expected_another_updated_at = user_password.updated_at, another_password.updated_at

    with freezegun.freeze_time(now() + timedelta(days=10)):
        token = encode_payload(access_payload(user_with_password))

        response = reset(client, user_with_password.id, token, ANOTHER_USER_PASSWORD, new_password)
        user_password.refresh_from_db()
        another_password.refresh_from_db()

        assert response.status_code == 422
        assert response.json() == PREVIOUS_PASSWORD_IS_WRONG_RESPONSE

        assert checkpw(USER_PASSWORD.encode(), user_password.value.encode())
        assert user_password.updated_at == expected_user_updated_at

        assert checkpw(ANOTHER_USER_PASSWORD.encode(), another_password.value.encode())
        assert another_password.updated_at == expected_another_updated_at


@pytest.mark.integration
@pytest.mark.django_db
def test_reset_password__if_prev_password_equals_new_with_new_password_values(
    client: Client, user_with_password: User, new_password="new password"
) -> None:
    _test_validation_unique_passwords(client, user_with_password, new_password)


@pytest.mark.integration
@pytest.mark.django_db
def test_reset_password__if_prev_password_equals_new_with_prev_password_values(
    client: Client,
    user_with_password: User,
) -> None:
    _test_validation_unique_passwords(client, user_with_password, USER_PASSWORD)


def _test_validation_unique_passwords(client: Client, user_with_password: User, password_value: str) -> None:
    password = user_with_password.password
    expected_updated_at = password.updated_at

    with freezegun.freeze_time(now() + timedelta(days=10)):
        token = encode_payload(access_payload(user_with_password))

        response = reset(client, user_with_password.id, token, password_value, password_value)
        password.refresh_from_db()

        assert response.status_code == 422
        assert checkpw(USER_PASSWORD.encode(), password.value.encode())
        assert password.updated_at == expected_updated_at


@pytest.mark.integration
@pytest.mark.django_db
def test_reset_password__if_jwt_token_does_not_belong_user_with_path_id(
    client: Client, user_token: str, another_user_with_password: User
) -> None:
    response = reset(client, another_user_with_password.id, user_token, "a", "b")

    assert response.status_code == 403
    assert response.json() == forbidden(ONLY_SELF)
    assert checkpw(ANOTHER_USER_PASSWORD.encode(), another_user_with_password.password.value.encode())


@pytest.mark.integration
@pytest.mark.django_db
def test_reset_password__if_path_user_id_is_not_existed_in_db(client: Client, user: User, user_token: str) -> None:
    response = reset(client, 0, user_token, "a", "b")

    assert response.status_code == 403
    assert response.json() == forbidden(ONLY_SELF)
