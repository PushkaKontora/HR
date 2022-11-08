import pytest
from django.test import Client
from ninja.responses import Response

from api.models import Vacancy
from tests.v1.integrations.conftest import get, not_found
from tests.v1.integrations.vacancies.conftest import VACANCY, vacancy_out


def get_vacancy(client: Client, vacancy_id: int) -> Response:
    return get(client, VACANCY.format(vacancy_id=vacancy_id))


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_vacancy(client: Client, vacancy: Vacancy) -> None:
    response = get_vacancy(client, vacancy.id)

    assert response.status_code == 200
    assert response.json() == vacancy_out(vacancy)


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_unknown_vacancy(client: Client, vacancy: Vacancy) -> None:
    assert vacancy.id != 0

    response = get_vacancy(client, 0)

    assert response.status_code == 404
    assert response.json() == not_found()
