from datetime import datetime
from typing import Optional

import freezegun
import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import FavouriteResume, Resume, User
from tests.v1.integrations.conftest import forbidden, not_found, patch, success
from tests.v1.integrations.resumes.conftest import RESUME

UNPUBLISH = RESUME + "/unpublish"


def unpublish(client: Client, resume_id: int, token: str) -> Response:
    return patch(client, UNPUBLISH.format(resume_id=resume_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_unpublish_resume__after_publish_state(
    client: Client, resume: Resume, another_user: User, user_token: str
) -> None:
    favourite = FavouriteResume.objects.create(user=another_user, resume=resume)

    _test_unpublish_resume(client, resume, another_user, user_token, published_at=now())

    assert not FavouriteResume.objects.filter(pk=favourite.pk).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_unpublish_resume__alter_unpublish_state(
    client: Client, resume: Resume, another_user: User, user_token: str
) -> None:
    _test_unpublish_resume(client, resume, another_user, user_token, published_at=None)


def _test_unpublish_resume(
    client: Client, resume: Resume, another_user: User, user_token: str, published_at: Optional[datetime]
) -> None:
    resume.published_at = published_at
    resume.save()

    response = unpublish(client, resume.id, user_token)

    assert response.status_code == 200
    assert response.json() == success()

    resume.refresh_from_db()
    assert resume.published_at is None


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_unpublish_resume__user_has_not_resume(
    client: Client, resume: Resume, user_token: str, another_user: User
) -> None:
    resume.owner = another_user
    resume.published_at = now()
    resume.save()

    response = unpublish(client, resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    resume.refresh_from_db()
    assert resume.published_at == now()


@pytest.mark.integration
@pytest.mark.django_db
def test_unpublish_resume__that_does_not_belong_to_authenticated_user(
    client: Client, resume: Resume, user_token: str, another_user: User
) -> None:
    expected_published_at = resume.published_at
    another_resume = Resume.objects.create(owner=another_user, desired_job="123")

    response = unpublish(client, another_resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    resume.refresh_from_db()
    assert resume.published_at == expected_published_at


@pytest.mark.integration
@pytest.mark.django_db
def test_publish_unknown_resume(client: Client, resume: Resume, user_token: str) -> None:
    assert resume.id != 0

    response = unpublish(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()
