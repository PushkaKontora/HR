from typing import List, Optional, Tuple
from unittest import mock
from unittest.mock import PropertyMock

import pytest
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.test import Client

from api.models import Competency, Experience, Resume, User
from tests.v1.integrations.conftest import error_422, forbidden, get_headers, success
from tests.v1.integrations.resumes.conftest import RESUMES, resume_out

CREATE_RESUME = RESUMES


def create(
    client: Client,
    token: str,
    user_id: int,
    desired_job: str,
    document: SimpleUploadedFile,
    desired_salary: int = None,
    experience: Experience = None,
    competencies: List[str] = None,
):

    body = {
        "user_id": user_id,
        "desired_job": desired_job,
        "document": document,
        "desired_salary": desired_salary,
        "experience": experience.value if experience else None,
        "competencies": competencies,
    }

    for key in list(body.keys()):
        if body[key] is None:
            del body[key]

    return client.post(CREATE_RESUME, body, **get_headers(token))


@pytest.mark.integration
@pytest.mark.django_db
def test_create_resume(
    client: Client,
    user: User,
    user_token: str,
    pdf_document: SimpleUploadedFile,
    desired_job: Optional[str] = "Frontend",
    desired_salary: Optional[int] = 100,
    experience: Optional[Experience] = Experience.NO_EXPERIENCE,
    competencies: Optional[Tuple] = ("Simpsons", "redux", "angular"),
) -> None:
    expected_competencies = competencies[1:] if competencies else None

    if expected_competencies:
        Competency.objects.bulk_create(Competency(name=n) for n in expected_competencies)

    response = create(client, user_token, user.id, desired_job, pdf_document, desired_salary, experience, competencies)
    resume = Resume.objects.get(owner=user)

    assert response.status_code == 200
    assert response.json() == resume_out(resume)

    assert resume.desired_job == desired_job
    assert resume.experience == experience
    assert resume.desired_salary == desired_salary
    if expected_competencies:
        assert set(resume.competencies.values_list("name", flat=True)) == set(expected_competencies)
    else:
        assert resume.competencies.count() == 0
    assert resume.published_at is None


@pytest.mark.integration
@pytest.mark.django_db
def test_create_resume__with_null_parameters(
    client: Client, user: User, user_token: str, pdf_document: SimpleUploadedFile
) -> None:
    test_create_resume(client, user, user_token, pdf_document, desired_salary=None, experience=None, competencies=None)


@pytest.mark.integration
@pytest.mark.django_db
def test_create_resume__document_is_not_pdf(
    client: Client, user: User, user_token: str, pdf_document: SimpleUploadedFile
) -> None:
    pdf_document.content_type = "image/png"

    response = create(client, user_token, user.id, "123", pdf_document)

    assert response.status_code == 422
    assert response.json() == error_422(2, "The attached document is not a pdf file")


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
def test_create_resume__document_size_is_large(
    client: Client, user: User, user_token: str, pdf_document: SimpleUploadedFile, size: int
) -> None:

    with mock.patch.object(UploadedFile, "size", new_callable=PropertyMock, return_value=size):
        response = create(client, user_token, user.id, "123", pdf_document)

    assert response.status_code == 422
    assert response.json() == error_422(
        5, f"The attached document size must be lte than {settings.MAX_FILE_SIZE_BYTES} bytes"
    )


@pytest.mark.integration
@pytest.mark.django_db
def test_create_resume__that_has_already_created(
    client: Client, user: User, user_token: str, pdf_document: SimpleUploadedFile, desired_job="Frontend"
) -> None:
    resume = Resume.objects.create(owner=user, desired_job="123")

    response = create(client, user_token, user.id, desired_job, pdf_document)

    assert response.status_code == 422
    assert response.json() == error_422(1, "The user has already created a resume")

    assert user.resume == resume


@pytest.mark.inegration
@pytest.mark.django_db
def test_create_resume__authenticated_user_try_it_with_another(
    client: Client,
    user: User,
    user_token: str,
    another_user: User,
    pdf_document: SimpleUploadedFile,
    desired_job="Frontend",
) -> None:
    response = create(client, user_token, another_user.id, desired_job, pdf_document)

    assert response.status_code == 403
    assert response.json() == forbidden()

    assert not Resume.objects.filter(owner=user).exists()
    assert not Resume.objects.filter(owner=another_user).exists()
