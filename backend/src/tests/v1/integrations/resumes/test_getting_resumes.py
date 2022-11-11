from typing import List, Optional, Set
from unittest import mock
from unittest.mock import PropertyMock

import pytest
from django.test import Client
from django.utils.timezone import now
from ninja.responses import Response

from api.models import Competency, Experience, Resume, ResumeCompetency, User
from tests.v1.integrations.conftest import forbidden, get
from tests.v1.integrations.resumes.conftest import RESUMES
from tests.v1.integrations.resumes.test_getting_resume import resume_out


def get_resumes(
    client: Client,
    token: str,
    search: Optional[str] = None,
    experience: Optional[Experience] = None,
    salary_from: Optional[int] = None,
    salary_to: Optional[int] = None,
    competencies: Optional[Set[str]] = None,
    published: Optional[bool] = None,
) -> Response:
    params = {
        "search": search,
        "experience": experience.value if experience else None,
        "salary_from": salary_from,
        "salary_to": salary_to,
        "published": published,
    }

    for key in list(params.keys()):
        if params[key] is None:
            del params[key]

    competencies_in = "" if not competencies else "&".join(map(lambda comp: f"competencies={comp}", competencies))
    params_in = "&".join(map(lambda p: f"{p[0]}={p[1]}", params.items()))
    uri = f"{RESUMES}?{params_in}&{competencies_in}"

    return get(client, uri, token)


def resumes_out(resumes: List[Resume]) -> dict:
    return {"items": [resume_out(resume) for resume in resumes], "count": len(resumes)}


@pytest.mark.integration
@pytest.mark.django_db
def test_get_resumes_by_employer_without_filters(client: Client, user: User, another_user, employer_token: str) -> None:
    resumes = Resume.objects.bulk_create(Resume(owner=usr, desired_job="123") for usr in (user, another_user))

    document = PropertyMock()
    document.url = "https://lima_dykov.gg"
    with mock.patch.object(Resume, "document", new_callable=PropertyMock, return_value=document):
        response = get_resumes(client, employer_token)

        assert response.status_code == 200
        assert response.json() == resumes_out(resumes)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_resumes_by_user_without_filters(client: Client, user_token: str) -> None:
    response = get_resumes(client, user_token)

    assert response.status_code == 403
    assert response.json() == forbidden()


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize("experience", Experience)
def test_get_resumes_by_employer_filtering_by_experience(
    client: Client, employer_token: str, experience: Experience
) -> None:
    resumes = Resume.objects.bulk_create(
        Resume(
            owner=User.objects.create(email=f"{num}@{num}.ru", surname="a", name="b", patronymic="c"),
            desired_job="123",
            experience=exp,
        )
        for num, exp in enumerate(Experience)
    )

    document = PropertyMock()
    document.url = "https://lima_dykov.gg"
    with mock.patch.object(Resume, "document", new_callable=PropertyMock, return_value=document):
        response = get_resumes(client, employer_token, experience=experience)

        assert response.status_code == 200
        assert response.json() == resumes_out(list(filter(lambda r: r.experience == experience, resumes)))


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(
    ["salary_from", "salary_to", "expected_resumes"],
    [
        [100, None, {1, 2, 3}],
        [101, None, {2, 3}],
        [None, 100, {1}],
        [None, 99, {}],
        [1001, None, {}],
        [100, 300, {1, 2}],
        [300, 300, {2}],
    ],
)
def test_get_resumes_by_employer_filtering_by_salary(
    client: Client,
    employer_token: str,
    salary_from: Optional[int],
    salary_to: Optional[int],
    expected_resumes: Set[int],
    salaries=(100, 300, 1000),
) -> None:
    resume_1, resume_2, resume_3 = Resume.objects.bulk_create(
        Resume(
            owner=User.objects.create(email=f"{num}@{num}.ru", surname="a", name="b", patronymic="c"),
            desired_job="123",
            desired_salary=salary,
        )
        for num, salary in enumerate(salaries)
    )

    resumes = {1: resume_1, 2: resume_2, 3: resume_3}

    document = PropertyMock()
    document.url = "https://lima_dykov.gg"
    with mock.patch.object(Resume, "document", new_callable=PropertyMock, return_value=document):
        response = get_resumes(client, employer_token, salary_from=salary_from, salary_to=salary_to)

        assert response.status_code == 200
        assert response.json() == resumes_out([resumes[key] for key in expected_resumes])


@pytest.mark.integration
@pytest.mark.django_db
@pytest.mark.parametrize(
    ["competencies_in", "expected_resumes"],
    [
        [{"redux"}, {1}],
        [{"django"}, {3}],
        [{"angular"}, {1, 2}],
        [{"redux", "angular"}, {1, 2}],
        [{"redux", "angular", "django"}, {1, 2, 3}],
        [{"angular", "django"}, {1, 2, 3}],
        [{"unknown"}, {}],
    ],
)
def test_get_resumes_by_employer_filtering_by_competencies(
    client: Client,
    employer_token: str,
    competencies_in: Set[str],
    expected_resumes: Set[int],
    competencies=("redux", "angular", "django"),
) -> None:
    redux, angular, django = Competency.objects.bulk_create(Competency(name=name) for name in competencies)

    users = User.objects.bulk_create(
        User(email=f"{num}@{num}.ru", surname=str(num), name=str(num), patronymic=str(num)) for num in range(3)
    )

    resume_1, resume_2, resume_3 = Resume.objects.bulk_create(
        Resume(owner=usr, desired_job=str(num)) for num, usr in enumerate(users)
    )
    ResumeCompetency.objects.bulk_create(
        ResumeCompetency(resume=resume_1, competency=comp) for comp in [redux, angular]
    )
    ResumeCompetency.objects.bulk_create(ResumeCompetency(resume=resume_2, competency=comp) for comp in [angular])
    ResumeCompetency.objects.bulk_create(ResumeCompetency(resume=resume_3, competency=comp) for comp in [django])

    resumes = {1: resume_1, 2: resume_2, 3: resume_3}
    document = PropertyMock()
    document.url = "https://lima_dykov.gg"
    with mock.patch.object(Resume, "document", new_callable=PropertyMock, return_value=document):
        response = get_resumes(client, employer_token, competencies=competencies_in)

        assert response.status_code == 200
        assert response.json() == resumes_out([resumes[key] for key in expected_resumes])


@pytest.mark.integration
@pytest.mark.django_db
def test_get_resumes_by_employer_filtering_by_published(
    client: Client, user: User, another_user: User, employer_token: str
) -> None:
    published_resume, unpublished_resume = Resume.objects.bulk_create(
        Resume(owner=usr, desired_job="1", published_at=pub) for usr, pub in [[user, now()], [another_user, None]]
    )

    document = PropertyMock()
    document.url = "https://lima_dykov.gg"
    with mock.patch.object(Resume, "document", new_callable=PropertyMock, return_value=document):
        _test_get_resume_by_published(client, employer_token, True, published_resume)
        _test_get_resume_by_published(client, employer_token, False, unpublished_resume)


def _test_get_resume_by_published(client: Client, employer_token: str, published: bool, resume: Resume) -> None:
    response = get_resumes(client, employer_token, published=published)

    assert response.status_code == 200
    assert response.json() == resumes_out([resume])
