from typing import List, Optional, Tuple

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from ninja.responses import Response

from api.models import Competency, Experiences, Resume, ResumeCompetency, User
from tests.v1.integrations.conftest import error_422, forbidden, get_headers, not_found, success
from tests.v1.integrations.resumes.conftest import RESUME

UPDATE = RESUME


def update(
    client: Client,
    resume_id: int,
    token: str,
    desired_job: str,
    document: SimpleUploadedFile,
    desired_salary: int = None,
    experience: Experiences = None,
    competencies: List[str] = None,
) -> Response:
    body = {
        "desired_job": desired_job,
        "document": document,
        "desired_salary": desired_salary,
        "experience": experience.value if experience else None,
        "competencies": competencies,
    }

    for key in list(body.keys()):
        if body[key] is None:
            del body[key]

    return client.post(UPDATE.format(resume_id=resume_id), body, **get_headers(token))


@pytest.mark.integration
@pytest.mark.django_db
def test_update_resume(
    client: Client,
    resume: Resume,
    user_token: str,
    pdf_document: Optional[SimpleUploadedFile],
    desired_job: str = "Frontend",
    desired_salary: Optional[int] = 100,
    experience: Optional[Experiences] = Experiences.NO_EXPERIENCE,
    competencies: Optional[Tuple] = ("Simpsons", "redux", "angular"),
) -> None:
    expected_competencies = competencies[1:] if competencies else None
    expected_document = resume.document

    if expected_competencies:
        created_competencies = Competency.objects.bulk_create(Competency(name=n) for n in expected_competencies)
        ResumeCompetency.objects.create(resume=resume, competency=created_competencies[0])

    response = update(
        client, resume.id, user_token, desired_job, pdf_document, desired_salary, experience, competencies
    )

    assert response.status_code == 200
    assert response.json() == success()

    resume.refresh_from_db()
    assert resume.desired_job == desired_job
    assert resume.experience == experience
    assert resume.desired_salary == desired_salary
    if expected_competencies:
        assert set(resume.competencies.values_list("name", flat=True)) == set(expected_competencies)
    else:
        assert resume.competencies.count() == 0

    if pdf_document is not None:
        pdf_document.seek(0)
        assert resume.document.read() == pdf_document.read()
    else:
        assert resume.document == expected_document


@pytest.mark.integration
@pytest.mark.django_db
def test_update_resume__with_null_parameters(
    client: Client, resume: Resume, user_token: str, pdf_document: SimpleUploadedFile
) -> None:
    test_update_resume(
        client, resume, user_token, pdf_document=None, desired_salary=None, experience=None, competencies=None
    )


@pytest.mark.integration
@pytest.mark.django_db
def test_update_resume__document_is_not_pdf(
    client: Client, resume: Resume, user_token: str, pdf_document: SimpleUploadedFile
) -> None:
    pdf_document.content_type = "image/png"

    response = update(client, resume.id, user_token, "123", pdf_document)

    assert response.status_code == 422
    assert response.json() == error_422(2, "The attached document is not a pdf file")


@pytest.mark.integration
@pytest.mark.django_db
def test_update_resume_that_does_not_belong_to_authenticated_user(
    client: Client, resume: Resume, user_token: str, another_user: User, pdf_document: SimpleUploadedFile
) -> None:
    resume.owner = another_user
    resume.save()

    response = update(client, resume.id, user_token, "123", pdf_document)

    assert response.status_code == 403
    assert response.json() == forbidden()

    assert Resume.objects.get(pk=resume.pk) == resume


@pytest.mark.integration
@pytest.mark.django_db
def test_update_unknown_resume(
    client: Client, resume: Resume, user_token: str, pdf_document: SimpleUploadedFile
) -> None:
    assert resume.id != 0

    response = update(client, 0, user_token, "123", pdf_document)

    assert response.status_code == 404
    assert response.json() == not_found()


@pytest.fixture(autouse=True)
def delete_uploaded_files() -> None:
    yield

    for resume in Resume.objects.all():
        resume.document.delete()
