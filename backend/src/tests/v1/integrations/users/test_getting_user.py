import pytest
from django.test import Client
from ninja.responses import Response

from api.models import Department, Resume, User
from tests.v1.integrations.conftest import datetime_to_string, get, not_found
from tests.v1.integrations.users.conftest import USER


def get_user(client: Client, user_id: int, token: str) -> Response:
    return get(client, USER.format(user_id=user_id), token)


def user_out(user: User) -> dict:
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
def test_get_one__when_resume_and_department_are_none(
    client: Client, user_with_password: User, user_token: str
) -> None:
    response = get_user(client, user_with_password.id, user_token)

    assert response.status_code == 200
    assert response.json() == user_out(user_with_password)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__with_resume(client: Client, user_with_password: User, user_token: str) -> None:
    Resume.objects.create(
        owner=user_with_password,
        desired_job="abc",
    )

    response = get_user(client, user_with_password.id, user_token)

    assert response.status_code == 200
    assert response.json() == user_out(user_with_password)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__with_department(client: Client, user_with_password: User, user_token: str) -> None:
    Department.objects.create(leader=user_with_password, name="asdf", description="asdf")

    response = get_user(client, user_with_password.id, user_token)

    assert response.status_code == 200
    assert response.json() == user_out(user_with_password)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__unknown_user_id(client: Client, user: User, user_token: str) -> None:
    response = get_user(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_user_by_employer(client: Client, user_with_password: User, employer_token: str) -> None:
    response = get_user(client, user_with_password.id, employer_token)

    assert response.status_code == 200
    assert response.json() == user_out(user_with_password)
