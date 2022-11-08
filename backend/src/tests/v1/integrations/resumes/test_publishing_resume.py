from datetime import datetime, timedelta

import freezegun
import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import Resume, User
from tests.v1.integrations.conftest import datetime_to_string, forbidden, not_found, patch
from tests.v1.integrations.resumes.conftest import RESUME

PUBLISH = RESUME + "/publish"


def publish(client: Client, resume_id: int, token: str) -> Response:
    return patch(client, PUBLISH.format(resume_id=resume_id), token)


def published_at_out(time: datetime) -> dict:
    return {"published_at": datetime_to_string(time)}


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_publish_resume__after_unpublish_state(client: Client, resume: Resume, user_token: str) -> None:
    resume.published_at = None
    resume.save(update_fields=["published_at"])

    response = publish(client, resume.id, user_token)

    assert response.status_code == 200
    assert response.json() == published_at_out(now())

    resume.refresh_from_db()
    assert resume.published_at == now()


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_publish_resume__after_publish_state(client: Client, resume: Resume, user_token: str) -> None:
    resume.published_at = now()
    resume.save(update_fields=["published_at"])

    with freezegun.freeze_time(now() + timedelta(seconds=1)):
        response = publish(client, resume.id, user_token)

    assert response.status_code == 200
    assert response.json() == published_at_out(now())

    resume.refresh_from_db()
    assert resume.published_at == now()


@pytest.mark.integration
@pytest.mark.django_db
@freezegun.freeze_time(now())
def test_publish_resume__user_has_not_resume(
    client: Client, resume: Resume, user_token: str, another_user: User
) -> None:
    resume.owner = another_user
    resume.published_at = now()
    resume.save()

    response = publish(client, resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    resume.refresh_from_db()
    assert resume.published_at == now()


@pytest.mark.integration
@pytest.mark.django_db
def test_publish_resume__that_does_not_belong_to_authenticated_user(
    client: Client, resume: Resume, user_token: str, another_user: User
) -> None:
    expected_published_at = resume.published_at
    another_resume = Resume.objects.create(owner=another_user, desired_job="123")

    response = publish(client, another_resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    resume.refresh_from_db()
    assert resume.published_at == expected_published_at


@pytest.mark.integration
@pytest.mark.django_db
def test_publish_unknown_resume(client: Client, resume: Resume, user_token: str) -> None:
    assert resume.id != 0

    response = publish(client, 0, user_token)

    assert response.status_code == 404
    assert response.json() == not_found()
