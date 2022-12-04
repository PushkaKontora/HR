import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from ninja.responses import Response

from api.models import Resume, User
from tests.v1.integrations.conftest import delete, forbidden, not_found, success
from tests.v1.integrations.resumes.conftest import RESUME

DOCUMENT = RESUME + "/document"


def delete_document(client: Client, resume_id: int, token: str) -> Response:
    return delete(client, DOCUMENT.format(resume_id=resume_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_document(
    client: Client, user: User, resume: Resume, user_token: str, pdf_document: SimpleUploadedFile
) -> None:
    resume.owner = user
    resume.document = pdf_document
    resume.save()

    _test_delete(client, resume, user_token)


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_document_that_has_deleted(client: Client, user: User, resume: Resume, user_token: str) -> None:
    resume.owner = user
    resume.document = None
    resume.save()

    _test_delete(client, resume, user_token)


def _test_delete(client: Client, resume: Resume, token: str) -> None:
    response = delete_document(client, resume.id, token)

    assert response.status_code == 200
    assert response.json() == success()

    resume.refresh_from_db()
    assert bool(resume.document) is False


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_document_at_resume_that_does_not_belong_to_authenticated_user(
    client: Client, resume: Resume, user_token: str, another_user: User
) -> None:
    resume.owner = another_user
    resume.save()

    response = delete_document(client, resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_document_at_unknown_resume(client: Client, resume: Resume, user_token: str) -> None:
    assert resume.id != 0

    response = delete_document(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()
