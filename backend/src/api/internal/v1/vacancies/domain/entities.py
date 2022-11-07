from datetime import datetime
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import Field, validator

from api.models import Experience, Vacancy


class VacanciesSortParameters(Enum):
    NAME = "name"
    PUBLISHED_AT = "published_at"
    SALARY_ASC = "salary_asc"
    SALARY_DESC = "salary_desc"


class VacanciesWishlistSortBy(Enum):
    PUBLISHED_AT_ASC = "published_at_asc"
    ADDED_AT_DESC = "added_at_desc"


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


class VacanciesWishlistParams(Schema):
    sort_by: VacanciesWishlistSortBy


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
    description: Optional[str]
    expected_experience: Experience
    salary_from: Optional[int]
    salary_to: Optional[int]
    department: VacancyDepartmentOut
    published_at: Optional[datetime]

    @staticmethod
    def from_vacancy(vacancy: Vacancy) -> "VacancyOut":
        department = vacancy.department
        leader = department.leader

        return VacancyOut(
            id=vacancy.id,
            name=vacancy.name,
            description=vacancy.description,
            expected_experience=vacancy.expected_experience,
            salary_from=vacancy.salary_from,
            salary_to=vacancy.salary_to,
            department=VacancyDepartmentOut(
                id=department.id,
                name=department.name,
                leader=DepartmentLeaderOut(
                    id=leader.id, surname=leader.surname, name=leader.name, patronymic=leader.patronymic
                ),
            ),
            published_at=vacancy.published_at,
        )


class VacancyIn(Schema):
    department_id: int
    name: str
    description: Optional[str]
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
