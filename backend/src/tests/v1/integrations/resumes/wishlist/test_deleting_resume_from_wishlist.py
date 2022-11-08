import pytest
from django.test import Client
from ninja.responses import Response

from api.models import FavouriteResume, Resume, User
from tests.v1.integrations.conftest import delete, forbidden, not_found, success
from tests.v1.integrations.resumes.wishlist.conftest import WISHLIST_RESUME


def delete_from_wishlist(client: Client, resume_id: int, token: str) -> Response:
    return delete(client, WISHLIST_RESUME.format(resume_id=resume_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_resume_by_employer(client: Client, resume: Resume, employer: User, employer_token: str) -> None:
    FavouriteResume.objects.create(user=employer, resume=resume)

    response = delete_from_wishlist(client, resume.id, employer_token)

    assert response.status_code == 200
    assert response.json() == success()

    assert employer.favourite_resumes.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_resume_by_user(client: Client, resume: Resume, user: User, user_token: str) -> None:
    FavouriteResume.objects.create(user=user, resume=resume)

    response = delete_from_wishlist(client, resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    assert list(user.favourite_resumes.all()) == [resume]


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_resume_that_is_not_in_wishlist(
    client: Client, resume: Resume, employer: User, employer_token: str
) -> None:
    assert employer.favourite_resumes.count() == 0

    response = delete_from_wishlist(client, resume.id, employer_token)

    assert response.status_code == 404
    assert response.json() == not_found()

    assert employer.favourite_resumes.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_delete_resume_that_does_not_exist(client: Client, employer: User, employer_token: str) -> None:
    assert employer.favourite_resumes.count() == 0

    response = delete_from_wishlist(client, 0, employer_token)

    assert response.status_code == 404
    assert response.json() == not_found()

    assert employer.favourite_resumes.count() == 0
