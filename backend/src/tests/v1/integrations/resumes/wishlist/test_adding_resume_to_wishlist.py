import pytest
from django.test import Client
from ninja.responses import Response

from api.models import FavouriteResume, Resume, User
from tests.v1.integrations.conftest import error_422, forbidden, not_found, post, success
from tests.v1.integrations.resumes.wishlist.conftest import WISHLIST_RESUME


def add_resume_to_wishlist(client: Client, resume_id: int, token: str) -> Response:
    return post(client, WISHLIST_RESUME.format(resume_id=resume_id), token)


@pytest.mark.integration
@pytest.mark.django_db
def test_add_resume_to_wishlist_by_employer(
    client: Client, resume: Resume, employer: User, employer_token: str
) -> None:
    assert resume.owner != employer

    response = add_resume_to_wishlist(client, resume.id, employer_token)

    assert response.status_code == 200
    assert response.json() == success()

    assert list(employer.favourite_resumes.all()) == [resume]


@pytest.mark.integration
@pytest.mark.django_db
def test_add_resume_to_wishlist_by_user(
    client: Client, resume: Resume, user: User, another_user: User, user_token: str
) -> None:
    resume.owner = another_user
    resume.save()

    response = add_resume_to_wishlist(client, resume.id, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()

    assert user.favourite_resumes.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_add_resume_to_wishlist__if_resume_already_added_by_employer(
    client: Client, resume: Resume, employer: User, employer_token: str
) -> None:
    FavouriteResume.objects.create(user=employer, resume=resume)

    response = add_resume_to_wishlist(client, resume.id, employer_token)

    assert response.status_code == 422
    assert response.json() == error_422(3, "The resume already added to wishlist")

    assert list(employer.favourite_resumes.all()) == [resume]


@pytest.mark.integration
@pytest.mark.django_db
def test_add_unknown_resume_to_wishlist_by_employer(
    client: Client, resume: Resume, employer: User, employer_token: str
) -> None:
    assert resume.id != 0

    response = add_resume_to_wishlist(client, 0, employer_token)

    assert response.status_code == 404
    assert response.json() == not_found()

    assert employer.favourite_resumes.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_adding_unpublished_resume_by_employer(
    client: Client, resume: Resume, employer: User, employer_token: str
) -> None:
    resume.published_at = None
    resume.save()

    response = add_resume_to_wishlist(client, resume.id, employer_token)

    assert response.status_code == 422
    assert response.json() == error_422(4, "You cannot add an unpublished resume to wishlist")
    assert not employer.favourite_resumes.exists()
