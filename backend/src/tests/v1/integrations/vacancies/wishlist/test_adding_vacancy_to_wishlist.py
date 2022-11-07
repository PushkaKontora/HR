import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import FavouriteVacancy, User, Vacancy
from tests.v1.integrations.conftest import error_422, not_found, post, success
from tests.v1.integrations.vacancies.wishlist.conftest import VACANCY_WISHLIST


def add_vacancy_to_wishlist(client: Client, vacancy_id: int, token: str) -> Response:
    return post(client, VACANCY_WISHLIST.format(vacancy_id=vacancy_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_adding_published_vacancy_to_wishlist(client: Client, vacancy: Vacancy, user: User, user_token: str) -> None:
    assert user.favourite_vacancies.count() == 0

    vacancy.published_at = now()
    vacancy.save()

    response = add_vacancy_to_wishlist(client, vacancy.id, user_token)

    assert response.status_code == 200
    assert response.json() == success()
    assert list(user.favourite_vacancies.all()) == [vacancy]


@pytest.mark.integration
@pytest.mark.django_db
def test_adding_unpublished_vacancy_to_wishlist(client: Client, vacancy: Vacancy, user: User, user_token: str) -> None:
    assert user.favourite_vacancies.count() == 0

    vacancy.published_at = None
    vacancy.save()

    response = add_vacancy_to_wishlist(client, vacancy.id, user_token)

    assert response.status_code == 422
    assert response.json() == error_422(2, "You cannot add an unpublished vacancy to wishlist")
    assert user.favourite_vacancies.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_adding_unknown_vacancy_to_wishlist(client: Client, vacancy: Vacancy, user: User, user_token: str) -> None:
    assert vacancy.id != 0
    assert user.favourite_vacancies.count() == 0

    response = add_vacancy_to_wishlist(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()
    assert user.favourite_vacancies.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_adding_added_vacancy_to_wishlist(client: Client, vacancy: Vacancy, user: User, user_token: str) -> None:
    vacancy.published_at = now()
    vacancy.save()

    FavouriteVacancy.objects.create(user=user, vacancy=vacancy)

    response = add_vacancy_to_wishlist(client, vacancy.id, user_token)

    assert response.status_code == 422
    assert response.json() == error_422(3, "The vacancy already added to wishlist")
    assert list(user.favourite_vacancies.all()) == [vacancy]
