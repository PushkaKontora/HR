from typing import Optional

import freezegun
import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import Department, Experience, User, Vacancy
from tests.v1.integrations.conftest import error_422, forbidden, post, success
from tests.v1.integrations.vacancies.conftest import VACANCIES


def create(
    client: Client,
    employer_token: str,
    department_id: int,
    name: str,
    description: str,
    expected_experience: Experience,
    published: bool,
    salary_from: Optional[int] = None,
    salary_to: Optional[int] = None,
) -> Response:
    body = {
        "department_id": department_id,
        "name": name,
        "description": description,
        "expected_experience": expected_experience.value,
        "published": published,
        "salary_from": salary_from,
        "salary_to": salary_to,
    }

    return post(client, VACANCIES, employer_token, body)


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_creating_vacancy_by_employer(
    client: Client,
    employer: User,
    department: Department,
    employer_token: str,
    name: str = "Frontend developer",
    description: str = "I forgot to turn off the iron",
    expected_experience: Experience = Experience.NO_EXPERIENCE,
    published: bool = True,
    salary_from: Optional[int] = 10000,
    salary_to: Optional[int] = 20000,
) -> None:
    response = create(
        client, employer_token, department.id, name, description, expected_experience, published, salary_from, salary_to
    )

    assert response.status_code == 200
    assert response.json() == success()

    vacancy = Vacancy.objects.filter(department=department).last()
    assert vacancy.name == name
    assert vacancy.description == description
    assert vacancy.expected_experience == expected_experience
    assert vacancy.published_at == (now() if published else None)
    assert vacancy.salary_from == salary_from
    assert vacancy.salary_to == salary_to


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_vacancy_by_employer_but_he_is_not_leader_of_department(
    client: Client, employer_token: str, department: Department, another_employer: User
) -> None:
    another_department = Department.objects.create(leader=another_employer, name="1")

    response = create(client, employer_token, another_department.id, "a", "b", Experience.NO_EXPERIENCE, True)

    assert response.status_code == 403
    assert response.json() == forbidden()

    assert not Vacancy.objects.exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_vacancy_with_unknown_department_id(client: Client, employer_token: str) -> None:
    response = create(client, employer_token, 0, "a", "b", Experience.NO_EXPERIENCE, True)

    assert response.status_code == 422
    assert response.json() == error_422(1, "Unknown department_id")


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_vacancy_by_user(client: Client, user_token: str, department: Department) -> None:
    response = create(client, user_token, department.id, "a", "b", Experience.NO_EXPERIENCE, True)

    assert response.status_code == 403
    assert response.json() == forbidden()

    assert not Vacancy.objects.exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_vacancy_with_published_and_unpublished_states(
    client: Client, employer: User, department: Department, employer_token: str
) -> None:
    test_creating_vacancy_by_employer(client, employer, department, employer_token, published=True)
    test_creating_vacancy_by_employer(client, employer, department, employer_token, published=False)


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_vacancy_with_null_value_in_salaries(
    client: Client, employer: User, department: Department, employer_token: str
) -> None:
    test_creating_vacancy_by_employer(client, employer, department, employer_token, salary_from=None)
    test_creating_vacancy_by_employer(client, employer, department, employer_token, salary_to=None)
    test_creating_vacancy_by_employer(client, employer, department, employer_token, salary_from=None, salary_to=None)


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_vacancy_if_salary_to_gt_than_salary_from(
    client: Client, employer: User, department: Department, employer_token: str, salary_from=10, salary_to=9
) -> None:
    response = create(
        client,
        employer_token,
        department.id,
        "a",
        "b",
        Experience.NO_EXPERIENCE,
        True,
        salary_from=salary_from,
        salary_to=salary_to,
    )

    assert response.status_code == 422
    assert not Vacancy.objects.exists()
