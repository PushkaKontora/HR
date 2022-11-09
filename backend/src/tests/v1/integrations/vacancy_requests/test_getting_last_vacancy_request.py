import time

import pytest
from django.test import Client
from ninja.responses import Response

from api.models import User, Vacancy, VacancyRequest
from tests.v1.integrations.conftest import get, not_found
from tests.v1.integrations.vacancy_requests.conftest import VACANCY_REQUESTS, request_out

LAST = VACANCY_REQUESTS + "/last?vacancy_id={vacancy_id}"


def get_last_request(client: Client, vacancy_id: int, token: str) -> Response:
    return get(client, LAST.format(vacancy_id=vacancy_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_last_vacancy_request__empty_list(client: Client, vacancy: Vacancy, user_token: str) -> None:
    response = get_last_request(client, vacancy.id, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_last_vacancy_request(client: Client, vacancy: Vacancy, user: User, user_token: str) -> None:
    VacancyRequest.objects.create(owner=user, vacancy=vacancy)
    time.sleep(1 / 12)
    expected = VacancyRequest.objects.create(owner=user, vacancy=vacancy)

    response = get_last_request(client, vacancy.id, user_token)

    assert response.status_code == 200
    assert response.json() == request_out(expected)


@pytest.mark.integration
@pytest.mark.django_db
def test_getting_last_vacancy_request__unknown_vacancy(client: Client, user_token: str) -> None:
    response = get_last_request(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()
