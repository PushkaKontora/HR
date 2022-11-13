from typing import Optional
from unittest import mock
from unittest.mock import MagicMock, PropertyMock

import pytest
from dependency_injector import containers, providers
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.internal.v1.vacancy_requests.api import VacancyRequestsContainer
from api.models import User, Vacancy, VacancyRequest
from tests.v1.integrations.conftest import error_422, get_headers, not_found
from tests.v1.integrations.vacancy_requests.conftest import VACANCY_REQUESTS, request_out


@containers.override(VacancyRequestsContainer)
class OverridingContainer(containers.DeclarativeContainer):
    employer_notifier = providers.Singleton(MagicMock())


def create_request(client: Client, token: str, vacancy_id: int, resume: Optional[SimpleUploadedFile]) -> Response:
    data = {"vacancy_id": vacancy_id} | ({} if resume is None else {"resume": resume})

    return client.post(VACANCY_REQUESTS, data, **get_headers(token))


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_request(
    client: Client, user: User, vacancy: Vacancy, user_token: str, pdf_document: SimpleUploadedFile
) -> None:
    assert not VacancyRequest.objects.filter(owner=user).exists()
    vacancy.published_at = now()
    vacancy.save()

    response = create_request(client, user_token, vacancy.id, None)

    assert response.status_code == 200
    assert response.json() == request_out(VacancyRequest.objects.get(owner=user))


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_request_on_unknown_vacancy(client: Client, user: User, user_token: str) -> None:
    assert not VacancyRequest.objects.filter(owner=user).exists()

    response = create_request(client, user_token, 0, None)

    assert response.status_code == 404
    assert response.json() == not_found()
    assert not VacancyRequest.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_request_on_unpublished_vacancy(client: Client, user: User, user_token: str, vacancy: Vacancy) -> None:
    assert not VacancyRequest.objects.filter(owner=user).exists()
    vacancy.published_at = None
    vacancy.save()

    response = create_request(client, user_token, vacancy.id, None)

    assert response.status_code == 404
    assert response.json() == not_found()
    assert not VacancyRequest.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_creating_request__document_is_not_pdf(
    client: Client, user: User, user_token: str, vacancy: Vacancy, pdf_document: SimpleUploadedFile
) -> None:
    assert not VacancyRequest.objects.filter(owner=user).exists()
    vacancy.published_at = now()
    vacancy.save()
    pdf_document.content_type = "image/png"

    response = create_request(client, user_token, vacancy.id, pdf_document)

    assert response.status_code == 422
    assert response.json() == error_422(1, "The resume file is not pdf")
    assert not VacancyRequest.objects.filter(owner=user).exists()


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(
    "size",
    [
        settings.MAX_FILE_SIZE_BYTES + 1,
        settings.MAX_FILE_SIZE_BYTES + 3,
        settings.MAX_FILE_SIZE_BYTES * 2,
    ],
)
def test_creating_request_document_is_large(
    client: Client, user: User, user_token: str, vacancy: Vacancy, pdf_document: SimpleUploadedFile, size: int
) -> None:
    assert not VacancyRequest.objects.filter(owner=user).exists()
    vacancy.published_at = now()
    vacancy.save()

    with mock.patch.object(UploadedFile, "size", new_callable=PropertyMock, return_value=size):
        response = create_request(client, user_token, vacancy.id, pdf_document)

    assert response.status_code == 422
    assert response.json() == error_422(2, f"Size of resume file must be lte than {settings.MAX_FILE_SIZE_BYTES} bytes")
    assert not VacancyRequest.objects.filter(owner=user).exists()
