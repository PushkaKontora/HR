import pytest
from django.conf import settings
from loguru import logger

from api.models import Resume, User


def pytest_configure(config):
    logger.disable("")


@pytest.fixture(autouse=True)
def override_settings_and_clear() -> None:
    settings.DEBUG = True
    yield

    for user in User.objects.all():
        if user.photo:
            user.photo.delete()

    for resume in Resume.objects.all():
        if resume.document:
            resume.document.delete()
