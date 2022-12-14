import time
from unittest import mock
from unittest.mock import PropertyMock

import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.internal.v1.resumes.domain.entities import ResumesSortBy
from api.models import FavouriteResume, Resume, User
from tests.v1.integrations.conftest import forbidden, get
from tests.v1.integrations.resumes.conftest import resume_out
from tests.v1.integrations.resumes.wishlist.conftest import RESUMES_WISHLIST


def get_wishlist(client: Client, token: str, sort_by: ResumesSortBy) -> Response:
    return get(client, f"{RESUMES_WISHLIST}?sort_by={sort_by.value}", token)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_wishlist_by_employer(
    client: Client, user: User, another_user: User, employer: User, employer_token: str
) -> None:
    resumes = []
    for usr in (user, another_user, employer):
        resumes.append(Resume.objects.create(owner=usr, desired_job="123", published_at=now()))
        time.sleep(1 / 4)

    for res in resumes[::-1]:
        FavouriteResume.objects.create(user=employer, resume=res)
        time.sleep(1 / 4)

    document = PropertyMock()
    document.url = "https://lima_dykov.gg"
    with mock.patch.object(Resume, "document", new_callable=PropertyMock, return_value=document):
        _test_sort_by_published_at_asc(client, employer, employer_token)
        _test_sort_by_published_at_desc(client, employer, employer_token)
        _test_sort_by_added_at_desc(client, employer, employer_token)


def _test_sort_by_published_at_asc(client: Client, employer: User, employer_token: str) -> None:
    response = get_wishlist(client, employer_token, ResumesSortBy.PUBLISHED_AT_ASC)

    assert response.status_code == 200
    assert response.json() == [
        resume_out(favourite.resume)
        for favourite in FavouriteResume.objects.filter(user=employer).order_by("resume__published_at")
    ]


def _test_sort_by_published_at_desc(client: Client, employer: User, employer_token: str) -> None:
    response = get_wishlist(client, employer_token, ResumesSortBy.PUBLISHED_AT_DESC)

    assert response.status_code == 200
    assert response.json() == [
        resume_out(favourite.resume)
        for favourite in FavouriteResume.objects.filter(user=employer).order_by("-resume__published_at")
    ]


def _test_sort_by_added_at_desc(client: Client, employer: User, employer_token: str) -> None:
    response = get_wishlist(client, employer_token, ResumesSortBy.ADDED_AT_DESC)

    assert response.status_code == 200
    assert response.json() == [
        resume_out(favourite.resume)
        for favourite in FavouriteResume.objects.filter(user=employer).order_by("-added_at")
    ]


@pytest.mark.integration
@pytest.mark.django_db
def test_get_wishlist_by_user(client: Client, user_token: str) -> None:
    response = get_wishlist(client, user_token, ResumesSortBy.ADDED_AT_DESC)

    assert response.status_code == 403
    assert response.json() == forbidden()
