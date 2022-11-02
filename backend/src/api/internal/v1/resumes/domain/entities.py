from datetime import datetime
from enum import Enum
from typing import List, Optional

from ninja import Schema
from pydantic import EmailStr, Field, HttpUrl

from api.models import Experiences


class ResumesSortParameters(Enum):
    NAME = "name"
    PUBLISHED_AT = "published_at"
    LIKED_AT = "liked_at"


class ResumesFilters(Schema):
    search: Optional[str] = None
    experience: Optional[Experiences] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    competencies: Optional[List[str]] = None


class OwnerOut(Schema):
    surname: str
    name: str
    patronymic: str
    email: EmailStr


class ResumeOut(Schema):
    owner: OwnerOut
    desired_job: str
    desired_salary: Optional[int]
    experience: Optional[Experiences]
    document: HttpUrl
    published_at: Optional[datetime]
    competencies: List[str]


class ResumeIn(Schema):
    desired_job: str
    desired_salary: Optional[int] = Field(None, gte=0)
    experience: Optional[Experiences] = None
    competencies: Optional[List[str]] = None


class NewResumeIn(ResumeIn):
    user_id: int


class ResumesWishlistFilters(Schema):
    sort_by: ResumesSortParameters


class ResumesWishlistIn(Schema):
    resume_id: int


class PublishingOut(Schema):
    published_at: datetime
