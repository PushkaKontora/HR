from datetime import timedelta
from typing import Optional, Set

import freezegun
import pytest
from django.db.models import F, Q
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.internal.v1.vacancies.domain.entities import VacanciesSortBy
from api.models import Department, Experience, User, Vacancy
from tests.v1.integrations.conftest import get
from tests.v1.integrations.vacancies.conftest import VACANCIES, vacancies_out


def get_vacancies(
    client: Client,
    sort_by: VacanciesSortBy,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    expected_experience: Optional[Experience] = None,
    salary_from: Optional[int] = None,
    salary_to: Optional[int] = None,
    published: Optional[bool] = None,
) -> Response:
    params = {
        "search": search,
        "department_id": department_id,
        "experience": expected_experience.value if expected_experience else None,
        "salary_from": salary_from,
        "salary_to": salary_to,
        "published": published,
    }

    for key in list(params.keys()):
        if params[key] is None:
            del params[key]

    params_in = "&".join(map(lambda p: f"{p[0]}={p[1]}", params.items()))
    uri = f"{VACANCIES}?sort_by={sort_by.value}&{params_in}"

    return get(client, uri)


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_vacancies_sorting_by_name_asc(client: Client, department: Department) -> None:
    Vacancy.objects.bulk_create(
        Vacancy(department=department, name=name, expected_experience=Experience.NO_EXPERIENCE)
        for name in ["c", "b", "a"]
    )

    response = get_vacancies(client, VacanciesSortBy.NAME_ASC)

    assert response.status_code == 200
    assert response.json() == vacancies_out(Vacancy.objects.order_by("name"))


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_getting_vacancies_sorting_by_published_at_desc(client: Client, department: Department) -> None:
    Vacancy.objects.bulk_create(
        Vacancy(
            department=department,
            name="published",
            published_at=now() + delta,
            expected_experience=Experience.NO_EXPERIENCE,
        )
        for delta in [timedelta(seconds=i) for i in range(3)]
    )
    Vacancy.objects.bulk_create(
        Vacancy(
            department=department, name="unpublished", published_at=None, expected_experience=Experience.NO_EXPERIENCE
        )
        for _ in range(2)
    )

    response = get_vacancies(client, VacanciesSortBy.PUBLISHED_AT_DESC)

    assert response.status_code == 200
    assert response.json() == vacancies_out(Vacancy.objects.order_by(F("published_at").desc(nulls_last=True)))


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_vacancies_filtering_by_department_id(
    client: Client, department: Department, another_employer: User
) -> None:
    other = Department.objects.create(leader=another_employer, name="other")
    Vacancy.objects.bulk_create(
        Vacancy(department=other, name="other", expected_experience=Experience.NO_EXPERIENCE) for _ in range(3)
    )
    Vacancy.objects.bulk_create(
        Vacancy(department=department, name="department", expected_experience=Experience.NO_EXPERIENCE)
        for _ in range(3)
    )

    response = get_vacancies(client, VacanciesSortBy.NAME_ASC, department_id=department.id)

    assert response.status_code == 200
    assert response.json() == vacancies_out(Vacancy.objects.filter(department=department).order_by("name"))


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize("experience", Experience)
def test_getting_vacancies_filtering_by_experience(
    client: Client, department: Department, experience: Experience
) -> None:
    Vacancy.objects.bulk_create(
        Vacancy(department=department, name=str(num), expected_experience=exp) for num, exp in enumerate(Experience)
    )

    response = get_vacancies(client, VacanciesSortBy.NAME_ASC, expected_experience=experience)

    assert response.status_code == 200
    assert response.json() == vacancies_out(Vacancy.objects.filter(expected_experience=experience).order_by("name"))


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_vacancies_filtering_by_published_state(client: Client, department: Department) -> None:
    Vacancy.objects.bulk_create(
        Vacancy(
            department=department,
            name="published",
            published_at=now() + delta,
            expected_experience=Experience.NO_EXPERIENCE,
        )
        for delta in [timedelta(seconds=i) for i in range(3)]
    )
    Vacancy.objects.bulk_create(
        Vacancy(
            department=department, name="unpublished", published_at=None, expected_experience=Experience.NO_EXPERIENCE
        )
        for _ in range(2)
    )

    _test_getting_published_vacancies(client)
    _test_getting_unpublished_vacancies(client)


def _test_getting_published_vacancies(client: Client) -> None:
    response = get_vacancies(client, VacanciesSortBy.NAME_ASC, published=True)

    assert response.status_code == 200
    assert response.json() == vacancies_out(Vacancy.objects.filter(~Q(published_at=None)).order_by("name"))


def _test_getting_unpublished_vacancies(client: Client) -> None:
    response = get_vacancies(client, VacanciesSortBy.NAME_ASC, published=False)

    assert response.status_code == 200
    assert response.json() == vacancies_out(Vacancy.objects.filter(published_at=None).order_by("name"))


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(
    ["salary_from", "salary_to", "expected_vacancies"],
    [
        [10, None, {1, 2, 3}],
        [None, 20, {0, 2, 3}],
        [10, 20, {2, 3}],
        [None, None, {0, 1, 2, 3}],
        [11, None, {3}],
        [None, 19, {3}],
        [0, 10**5, {2, 3}],
        [-(10**5), 10**5, {2, 3}],
    ],
)
def test_getting_vacancies_filtering_by_salary(
    client: Client,
    department: Department,
    salary_from: Optional[int],
    salary_to: Optional[int],
    expected_vacancies: Set[int],
    salaries=((None, 20), (10, None), (10, 20), (11, 19)),
) -> None:
    vacancies = Vacancy.objects.bulk_create(
        Vacancy(
            department=department,
            salary_from=salary[0],
            salary_to=salary[1],
            expected_experience=Experience.NO_EXPERIENCE,
        )
        for salary in salaries
    )

    response = get_vacancies(client, VacanciesSortBy.NAME_ASC, salary_from=salary_from, salary_to=salary_to)

    assert response.status_code == 200
    assert response.json() == vacancies_out([vacancies[expected] for expected in expected_vacancies])
