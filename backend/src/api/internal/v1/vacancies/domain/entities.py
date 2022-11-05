from datetime import datetime
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import Field, validator

from api.models import Experience


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
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    experience: Optional[Experience] = None
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
    id: int
    name: str
    description: str
    expected_experience: Experience
    salary_from: Optional[int]
    salary_to: Optional[int]
    department: VacancyDepartmentOut
    published_at: Optional[datetime]


class VacancyIn(Schema):
    department_id: int
    name: str
    description: str
    expected_experience: Experience
    salary_from: Optional[int]
    salary_to: Optional[int]
    published: bool

    @validator("salary_to")
    @classmethod
    def validate_not_equality_of_passwords(cls, field_value, values, field, config):
        salary_to, salary_from = field_value, values["salary_from"]

        if salary_from is None or salary_to is None:
            return field_value

        if salary_from > salary_to:
            raise ValueError("A salary_from parameter must be less or equal than a salary_to parameter")

        return field_value


class VacanciesWishlistIn(Schema):
    vacancy_id: int


class PublishingOut(Schema):
    published_at: datetime


class RequestOut(Schema):
    updated_at: datetime
