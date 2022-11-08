import time

import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.internal.v1.vacancies.domain.entities import VacanciesWishlistSortBy
from api.models import Department, Experience, FavouriteVacancy, User, Vacancy
from tests.v1.integrations.conftest import get
from tests.v1.integrations.vacancies.conftest import vacancy_out
from tests.v1.integrations.vacancies.wishlist.conftest import VACANCIES_WISHLIST


def get_vacancies_wishlist(client: Client, token: str, sort_by: VacanciesWishlistSortBy) -> Response:
    return get(client, f"{VACANCIES_WISHLIST}?sort_by={sort_by.value}", token)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_vacancies_wishlist(client: Client, user: User, user_token: str, department: Department) -> None:
    vacancies = []
    for _ in range(3):
        vacancies.append(
            Vacancy.objects.create(
                department=department, name="123", published_at=now(), expected_experience=Experience.NO_EXPERIENCE
            )
        )
        time.sleep(1 / 4)

    for vacancy in vacancies[::-1]:
        FavouriteVacancy.objects.create(user=user, vacancy=vacancy)
        time.sleep(1 / 4)

    _test_sort_by_published_at_asc(client, user, user_token)
    _test_sort_by_added_at_desc(client, user, user_token)


def _test_sort_by_published_at_asc(client: Client, user: User, user_token: str) -> None:
    response = get_vacancies_wishlist(client, user_token, VacanciesWishlistSortBy.PUBLISHED_AT_ASC)

    assert response.status_code == 200
    assert response.json() == [vacancy_out(vacancy) for vacancy in user.favourite_vacancies.order_by("published_at")]


def _test_sort_by_added_at_desc(client: Client, user: User, user_token: str) -> None:
    response = get_vacancies_wishlist(client, user_token, VacanciesWishlistSortBy.ADDED_AT_DESC)

    assert response.status_code == 200
    assert response.json() == [
        vacancy_out(favourite.vacancy) for favourite in FavouriteVacancy.objects.filter(user=user).order_by("-added_at")
    ]
