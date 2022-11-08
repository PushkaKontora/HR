import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now

from api.models import Resume, User
from tests.v1.integrations.conftest import V1

RESUMES = V1 + "/resumes"
RESUME = RESUMES + "/{resume_id}"


@pytest.fixture
def pdf_document() -> SimpleUploadedFile:
    return SimpleUploadedFile("test_document.pdf", b"123", content_type="application/pdf")


@pytest.fixture
def resume(user: User) -> Resume:
    return Resume.objects.create(owner=user, desired_job="Frontend", published_at=now())
