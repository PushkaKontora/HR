from datetime import datetime
from typing import Optional

import freezegun
import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import Department, User, Vacancy
from tests.v1.integrations.conftest import forbidden, not_found, patch, success
from tests.v1.integrations.vacancies.conftest import VACANCY

UNPUBLISH = VACANCY + "/unpublish"


def unpublish(client: Client, vacancy_id: int, token: str) -> Response:
    return patch(client, UNPUBLISH.format(vacancy_id=vacancy_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_unpublishing_vacancy_by_user(client: Client, vacancy: Vacancy, user_token: str) -> None:
    expected_published_at = vacancy.published_at

    response = unpublish(client, vacancy.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    vacancy.refresh_from_db()
    assert vacancy.published_at == expected_published_at


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_unpublishing_vacancy_by_employer_after_publishing(
    client: Client, vacancy: Vacancy, employer_token: str
) -> None:
    _test_unpublishing_by_employer(client, vacancy, employer_token, published_at=now())


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_unpublishing_vacancy_by_employer_after_unpublishing(
    client: Client, vacancy: Vacancy, employer_token: str
) -> None:
    _test_unpublishing_by_employer(client, vacancy, employer_token, published_at=None)


def _test_unpublishing_by_employer(
    client: Client, vacancy: Vacancy, employer_token: str, published_at: Optional[datetime]
) -> None:
    vacancy.published_at = published_at
    vacancy.save()

    response = unpublish(client, vacancy.id, employer_token)

    assert response.status_code == 200
    assert response.json() == success()

    vacancy.refresh_from_db()
    assert vacancy.published_at is None


@pytest.mark.integration
@pytest.mark.django_db
def test_unpublishing_vacancy_by_employer_who_is_not_leader_of_department(
    client: Client, another_employer: User, department: Department, vacancy: Vacancy, employer_token: str
) -> None:
    department.leader = another_employer
    department.save()

    vacancy.published_at = now()
    vacancy.department = department
    vacancy.save()

    response = unpublish(client, vacancy.id, employer_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    vacancy.refresh_from_db()
    assert vacancy.published_at is not None


@pytest.mark.integration
@pytest.mark.django_db
def test_unpublishing_unknown_vacancy(client: Client, vacancy: Vacancy, employer_token: str) -> None:
    assert vacancy.id != 0

    response = unpublish(client, 0, employer_token)

    assert response.status_code == 404
    assert response.json() == not_found()

    assert Vacancy.objects.get(pk=vacancy.pk) == vacancy
