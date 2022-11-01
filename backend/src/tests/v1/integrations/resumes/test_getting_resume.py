import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from ninja.responses import Response

from api.models import Competency, Resume, ResumeCompetency, User
from tests.v1.integrations.conftest import forbidden, get, not_found
from tests.v1.integrations.resumes.conftest import RESUME


def get_one(client: Client, resume_id: int, token: str) -> Response:
    return get(client, RESUME.format(resume_id=resume_id), token)


def resume_out(resume: Resume) -> dict:
    owner = resume.owner
    return {
        "owner": {
            "surname": owner.surname,
            "name": owner.name,
            "patronymic": owner.patronymic,
            "email": owner.email,
        },
        "desired_job": resume.desired_job,
        "desired_salary": resume.desired_salary,
        "experience": resume.experience,
        "document": resume.document.url,
        "published_at": resume.published_at,
        "competencies": list(resume.competencies.values_list("name", flat=True)),
    }


@pytest.mark.integration
@pytest.mark.django_db
def test_get_resume__by_owner(
    client: Client, resume: Resume, pdf_document: SimpleUploadedFile, user: User, user_token: str
) -> None:
    assert resume.owner == user
    resume.document = pdf_document
    resume.save()

    competencies = Competency.objects.bulk_create(Competency(name=str(i)) for i in range(3))
    ResumeCompetency.objects.bulk_create(ResumeCompetency(resume=resume, competency=comp) for comp in competencies)

    response = get_one(client, resume.id, user_token)

    assert response.status_code == 200
    assert response.json() == resume_out(resume)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_resume__employer_has_access_to_any_resumes(
    client: Client, resume: Resume, employer: User, employer_token: str, pdf_document: SimpleUploadedFile
) -> None:
    assert resume.owner != employer
    resume.document = pdf_document
    resume.save()

    response = get_one(client, resume.id, employer_token)

    assert response.status_code == 200
    assert response.json() == resume_out(resume)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_resume__employer_has_access_to_his_resume(
    client: Client, employer: User, employer_token: str, pdf_document: SimpleUploadedFile
) -> None:
    resume = Resume.objects.create(owner=employer, desired_job="123", document=pdf_document)

    response = get_one(client, resume.id, employer_token)

    assert response.status_code == 200
    assert response.json() == resume_out(resume)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_resume__authenticated_user_cannot_get_anothers_resume(
    client: Client, user_token: str, another_user: User
) -> None:
    another_resume = Resume.objects.create(owner=another_user, desired_job="123")

    response = get_one(client, another_resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()


@pytest.fixture(autouse=True)
def delete_uploaded_files() -> None:
    yield

    for resume in Resume.objects.all():
        resume.document.delete()