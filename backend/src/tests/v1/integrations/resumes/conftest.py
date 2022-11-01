import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from tests.v1.integrations.conftest import V1

RESUMES = V1 + "/resumes"
RESUME = RESUMES + "/{resume_id}"


@pytest.fixture
def pdf_document() -> SimpleUploadedFile:
    return SimpleUploadedFile("test_document.pdf", b"123", content_type="application/pdf")
