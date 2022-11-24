import pytest
from django.utils.timezone import now

from api.models import Resume, User
from tests.v1.integrations.conftest import V1, datetime_to_string

RESUMES = V1 + "/resumes"
RESUME = RESUMES + "/{resume_id}"


@pytest.fixture
def resume(user: User) -> Resume:
    return Resume.objects.create(owner=user, desired_job="Frontend", published_at=now())


def resume_out(resume: Resume) -> dict:
    owner = resume.owner
    return {
        "id": resume.id,
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
        "published_at": datetime_to_string(resume.published_at) if resume.published_at else None,
        "competencies": list(resume.competencies.values_list("name", flat=True)),
    }
