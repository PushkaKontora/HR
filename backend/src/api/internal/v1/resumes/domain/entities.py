from datetime import datetime
from enum import Enum
from typing import List, Optional, Set

from django.conf import settings
from django.db.models import QuerySet
from ninja import Schema
from pydantic import EmailStr, Field, HttpUrl

from api.models import Experience, Resume


class ResumesSortBy(Enum):
    PUBLISHED_AT_DESC = "published_at_desc"
    PUBLISHED_AT_ASC = "published_at_asc"
    ADDED_AT_DESC = "added_at_desc"


class ResumesParams(Schema):
    published: Optional[bool] = None
    search: Optional[str] = None
    experience: Optional[Experience] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    competencies: Optional[Set[str]] = None
    limit: int = Field(settings.PAGINATION_PER_PAGE, ge=1)
    offset: int = Field(0, ge=0)


class OwnerOut(Schema):
    surname: str
    name: str
    patronymic: str
    email: EmailStr


class ResumeOut(Schema):
    id: int
    owner: OwnerOut
    desired_job: str
    desired_salary: Optional[int]
    experience: Optional[Experience]
    document: HttpUrl
    published_at: Optional[datetime]
    competencies: List[str]

    @staticmethod
    def from_resume(resume: Resume) -> "ResumeOut":
        owner = resume.owner

        return ResumeOut(
            id=resume.id,
            owner=OwnerOut(
                surname=owner.surname,
                name=owner.name,
                patronymic=owner.patronymic,
                email=owner.email,
            ),
            desired_job=resume.desired_job,
            desired_salary=resume.desired_salary,
            experience=resume.experience,
            document=resume.document.url,
            published_at=resume.published_at,
            competencies=list(resume.competencies.values_list("name", flat=True)),
        )


class ResumesOut(Schema):
    items: List[ResumeOut]
    count: int

    @staticmethod
    def from_resumes_with_pagination(resumes: QuerySet[Resume], limit: int, offset: int) -> "ResumesOut":
        return ResumesOut(
            items=[ResumeOut.from_resume(resume) for resume in resumes[offset : offset + limit]],
            count=resumes.count(),
        )


class ResumeIn(Schema):
    desired_job: str
    desired_salary: Optional[int] = Field(None, gte=0)
    experience: Optional[Experience] = None
    competencies: Optional[List[str]] = None


class NewResumeIn(ResumeIn):
    user_id: int


class ResumesWishlistParameters(Schema):
    sort_by: ResumesSortBy


class PublishingOut(Schema):
    published_at: datetime

    @staticmethod
    def from_resume(resume: Resume) -> "PublishingOut":
        return PublishingOut(published_at=resume.published_at)
