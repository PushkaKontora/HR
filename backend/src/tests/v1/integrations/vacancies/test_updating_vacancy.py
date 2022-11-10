from datetime import timedelta
from typing import Optional

import freezegun
import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import Department, Experience, User, Vacancy
from tests.v1.integrations.conftest import forbidden, not_found, put, success
from tests.v1.integrations.vacancies.conftest import VACANCY


def update_vacancy(
    client: Client,
    vacancy_id: int,
    token: str,
    name: str,
    expected_experience: Experience,
    salary_from: Optional[int],
    salary_to: Optional[int],
    published: bool,
) -> Response:
    body = {
        "name": name,
        "expected_experience": expected_experience,
        "salary_from": salary_from,
        "salary_to": salary_to,
        "published": published,
    }

    return put(client, VACANCY.format(vacancy_id=vacancy_id), token, body)


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time()
def test_updating_vacancy_by_employer(
    client: Client,
    vacancy: Vacancy,
    employer_token: str,
    name: str = "Frontend",
    expected_experience: Experience = Experience.NO_EXPERIENCE,
    salary_from: Optional[int] = 100,
    salary_to: Optional[int] = 200,
    published: bool = True,
) -> None:

    department_id = int(vacancy.department_id)
    response = update_vacancy(
        client, vacancy.id, employer_token, name, expected_experience, salary_from, salary_to, published
    )

    assert response.status_code == 200
    assert response.json() == success()

    vacancy.refresh_from_db()
    assert vacancy.department_id == department_id
    assert vacancy.name == name
    assert vacancy.expected_experience == expected_experience
    assert vacancy.salary_from == salary_from
    assert vacancy.salary_to == salary_to
    if published:
        assert vacancy.published_at == now()
    else:
        assert vacancy.published_at is None


@pytest.mark.integration
@pytest.mark.django_db
def test_updating_vacancy_by_employer_who_is_not_leader_of_the_department(
    client: Client,
    vacancy: Vacancy,
    department: Department,
    another_employer: User,
    employer_token: str,
    name: str = "Frontend",
    expected_experience: Experience = Experience.NO_EXPERIENCE,
    salary_from: Optional[int] = 100,
    salary_to: Optional[int] = 200,
    published: bool = True,
) -> None:
    department.leader = another_employer
    department.save()

    vacancy.department = department
    vacancy.save()

    response = update_vacancy(
        client, vacancy.id, employer_token, name, expected_experience, salary_from, salary_to, published
    )

    assert response.status_code == 403
    assert response.json() == forbidden()
    assert Vacancy.objects.get(pk=vacancy.pk) == vacancy


@pytest.mark.integration
@pytest.mark.django_db
def test_updating_vacancy_by_user(
    client: Client,
    vacancy: Vacancy,
    user_token: str,
    name: str = "Frontend",
    expected_experience: Experience = Experience.NO_EXPERIENCE,
    salary_from: Optional[int] = None,
    salary_to: Optional[int] = None,
    published: bool = True,
) -> None:
    response = update_vacancy(
        client, vacancy.id, user_token, name, expected_experience, salary_from, salary_to, published
    )

    assert response.status_code == 403
    assert response.json() == forbidden()
    assert Vacancy.objects.get(pk=vacancy.pk) == vacancy


@pytest.mark.integration
@pytest.mark.django_db
def test_updating_unknown_vacancy_by_employer(
    client: Client,
    vacancy: Vacancy,
    employer_token: str,
    name: str = "Frontend",
    expected_experience: Experience = Experience.NO_EXPERIENCE,
    salary_from: Optional[int] = 100,
    salary_to: Optional[int] = 200,
    published: bool = True,
) -> None:

    assert vacancy.id != 0

    response = update_vacancy(
        client,
        0,
        employer_token,
        name,
        expected_experience,
        salary_from,
        salary_to,
        published,
    )

    assert response.status_code == 404
    assert response.json() == not_found()
    assert Vacancy.objects.get(pk=vacancy.pk) == vacancy


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_updating_vacancy_by_employer_with_different_salaries(
    client: Client, vacancy: Vacancy, employer_token: str
) -> None:
    test_updating_vacancy_by_employer(client, vacancy, employer_token, salary_from=None)
    test_updating_vacancy_by_employer(client, vacancy, employer_token, salary_to=None)
    test_updating_vacancy_by_employer(client, vacancy, employer_token, salary_from=None, salary_to=None)


@pytest.mark.integration
@pytest.mark.django_db
def test_updating_vacancy_by_employer_with_different_published_param(
    client: Client, vacancy: Vacancy, employer_token: str
) -> None:
    test_updating_vacancy_by_employer(client, vacancy, employer_token, published=True)
    test_updating_vacancy_by_employer(client, vacancy, employer_token, published=False)


@pytest.mark.integration
@pytest.mark.django_db
def test_updating_vacancy_by_employer__salary_from_is_gt_than_salary_to(
    client: Client,
    vacancy: Vacancy,
    employer_token: str,
    name: str = "Frontend",
    expected_experience: Experience = Experience.NO_EXPERIENCE,
    salary_from: Optional[int] = 20,
    salary_to: Optional[int] = 10,
    published: bool = True,
) -> None:

    response = update_vacancy(
        client,
        vacancy.id,
        employer_token,
        name,
        expected_experience,
        salary_from,
        salary_to,
        published,
    )

    assert response.status_code == 422
    assert Vacancy.objects.get(pk=vacancy.pk) == vacancy


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_updating_vacancy_by_employer_alter_published_state(
    client: Client, vacancy: Vacancy, employer_token: str
) -> None:
    vacancy.published_at = now()
    vacancy.save()

    with freezegun.freeze_time(now() + timedelta(seconds=1)):
        response = update_vacancy(client, vacancy.id, employer_token, "a", Experience.NO_EXPERIENCE, 10, 20, True)

        assert response.status_code == 200
        assert response.json() == success()

        vacancy.refresh_from_db()
        assert vacancy.published_at == now()
