from unittest.mock import Mock

import pytest
from django.test import Client
from ninja.responses import Response

from api.models import Department, Resume, User
from tests.conftest import datetime_to_string, get, not_found_error
from tests.v1.integrations.users.conftest import USER


def get_one(client: Client, user_id: int) -> Response:
    return get(client, USER.format(user_id=user_id))


def get_expected_user_out(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "permission": str(user.permission),
        "surname": user.surname,
        "name": user.name,
        "patronymic": user.patronymic,
        "photo": user.photo.url if user.photo else None,
        "resume": {"id": user.resume.id} if hasattr(user, "resume") else None,
        "department": {"id": user.department.id} if hasattr(user, "department") else None,
        "password": {"updated_at": datetime_to_string(user.password.updated_at)},
    }


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__when_resume_and_department_are_none(client: Client, user_with_password: User) -> None:
    response = get_one(client, user_with_password.id)

    assert response.status_code == 200
    assert response.json() == get_expected_user_out(user_with_password)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__with_resume(client: Client, user_with_password: User) -> None:
    Resume.objects.create(
        owner=user_with_password,
        desired_job="abc",
    )

    response = get_one(client, user_with_password.id)

    assert response.status_code == 200
    assert response.json() == get_expected_user_out(user_with_password)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__with_department(client: Client, user_with_password: User) -> None:
    Department.objects.create(leader=user_with_password, name="asdf", description="asdf")

    response = get_one(client, user_with_password.id)

    assert response.status_code == 200
    assert response.json() == get_expected_user_out(user_with_password)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__unknown_user_id(client: Client, user: User) -> None:
    response = get_one(client, 0)

    assert response.status_code == 404
    assert response.json() == not_found_error()
