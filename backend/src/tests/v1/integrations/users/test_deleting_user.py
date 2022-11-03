import pytest
from django.test import Client
from ninja.responses import Response

from api.models import (
    Department,
    FavouriteResume,
    FavouriteVacancy,
    IssuedToken,
    Password,
    Resume,
    User,
    Vacancy,
    VacancyRequest,
)
from tests.v1.integrations.conftest import delete as _delete, error_422, forbidden, not_found, success
from tests.v1.integrations.users.conftest import USER


def delete(client: Client, user_id: int, token: str) -> Response:
    return _delete(client, USER.format(user_id=user_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_user(client: Client, user: User, user_token: str, another_user: User) -> None:
    department = Department.objects.create(leader=another_user, name="adf")
    another_resume = Resume.objects.create(owner=another_user, desired_job="q")
    another_vacancy = Vacancy.objects.create(department=department, name="aaa")

    Password.objects.create(owner=user, value="123")
    Resume.objects.create(owner=user, desired_job="abc")
    FavouriteResume.objects.create(user=user, resume=another_resume)
    FavouriteVacancy.objects.create(user=user, vacancy=another_vacancy)
    VacancyRequest.objects.create(owner=user, vacancy=another_vacancy)
    IssuedToken.objects.create(owner=user, value="1234")

    response = delete(client, user.id, user_token)

    assert response.status_code == 200
    assert response.json() == success()

    assert Department.objects.filter(pk=department.pk).exists()
    assert Resume.objects.filter(pk=another_resume.pk).exists()
    assert Vacancy.objects.filter(pk=another_vacancy.pk).exists()

    assert not Password.objects.filter(owner=user).exists()
    assert not Resume.objects.filter(owner=user).exists()
    assert not FavouriteResume.objects.filter(user=user).exists()
    assert not FavouriteVacancy.objects.filter(user=user).exists()
    assert not VacancyRequest.objects.filter(owner=user).exists()
    assert not IssuedToken.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_user__user_is_leader_of_department(client: Client, user: User, user_token: str) -> None:
    department = Department.objects.create(leader=user, name="adf")

    response = delete(client, user.id, user_token)

    assert response.status_code == 422
    assert response.json() == error_422(10, "The user is a leader of a department")
    assert User.objects.filter(pk=user.pk).exists()
    assert Department.objects.filter(pk=department.pk).exists()


@pytest.mark.integraion
@pytest.mark.django_db
def test_delete_user__authenticated_user_try_to_delete_another(
    client: Client, user: User, user_token: str, another_user: User
) -> None:
    response = delete(client, another_user.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()
    assert User.objects.filter(pk=user.pk).exists()
    assert User.objects.filter(pk=another_user.pk).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_user_with_unknown_id(client: Client, user: User, user_token: str) -> None:
    response = delete(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()

    assert User.objects.filter(pk=user.pk).exists()
