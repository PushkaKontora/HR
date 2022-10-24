from datetime import datetime
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import Field

from api.internal.models import Experiences


class VacanciesSortParameters(Enum):
    NAME = "name"
    PUBLISHED_AT = "published_at"
    SALARY_ASC = "salary_asc"
    SALARY_DESC = "salary_desc"


class VacanciesWishlistSortParameters(Enum):
    NAME = "name"
    LIKED_AT = "liked_at"


class VacanciesStatus(Enum):
    ALL = "all"
    PUBLISHED = "published"
    UNPUBLISHED = "unpublished"


class VacanciesFilters(Schema):
    search: Optional[str] = None
    department_name: Optional[str] = None
    experience: Optional[Experiences] = None
    salary_from: Optional[int] = Field(None, gte=0)
    salary_to: Optional[int] = Field(None, gte=0)
    status: VacanciesStatus
    sort_by: VacanciesSortParameters


class VacanciesWishlistFilters(Schema):
    sort_by: VacanciesWishlistSortParameters


class DepartmentLeaderOut(Schema):
    id: int
    surname: str
    name: str
    patronymic: str


class VacancyDepartmentOut(Schema):
    id: int
    name: str
    leader: DepartmentLeaderOut


class VacancyOut(Schema):
    name: str
    description: str
    expected_experience: Experiences
    salary_from: Optional[int]
    salary_to: Optional[int]
    department: VacancyDepartmentOut
    published_at: Optional[datetime]


class VacancyIn(Schema):
    name: str
    description: str
    expected_experience: Experiences
    salary_from: Optional[int]
    salary_to: Optional[int]
    published: bool


class VacanciesWishlistIn(Schema):
    vacancy_id: int


class PublishingOut(Schema):
    published_at: datetime


class RequestOut(Schema):
    updated_at: datetime
