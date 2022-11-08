import pytest
from django.test import Client
from ninja.responses import Response

from api.models import FavouriteVacancy, User, Vacancy
from tests.v1.integrations.conftest import delete, not_found, success
from tests.v1.integrations.vacancies.wishlist.conftest import VACANCY_WISHLIST


def delete_vacancy_from_wishlist(client: Client, vacancy_id: int, token: str) -> Response:
    return delete(client, VACANCY_WISHLIST.format(vacancy_id=vacancy_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_deleting_vacancy_from_wishlist(client: Client, vacancy: Vacancy, user: User, user_token: str) -> None:
    FavouriteVacancy.objects.create(user=user, vacancy=vacancy)

    response = delete_vacancy_from_wishlist(client, vacancy.id, user_token)

    assert response.status_code == 200
    assert response.json() == success()
    assert user.favourite_vacancies.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_deleting_not_added_vacancy_from_wishlist(
    client: Client, vacancy: Vacancy, user: User, user_token: str
) -> None:
    assert user.favourite_vacancies.count() == 0
    response = delete_vacancy_from_wishlist(client, vacancy.id, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()

    assert user.favourite_vacancies.count() == 0
    assert Vacancy.objects.filter(pk=vacancy.pk).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_deleting_unknown_vacancy_from_wishlist(client: Client, vacancy: Vacancy, user: User, user_token: str) -> None:
    assert user.favourite_vacancies.count() == 0
    assert vacancy.id != 0

    response = delete_vacancy_from_wishlist(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()
    assert user.favourite_vacancies.count() == 0
