from datetime import datetime
from enum import Enum
from typing import List, Optional

from django.conf import settings
from django.db.models import QuerySet
from ninja import Schema
from pydantic import Field, validator

from api.internal.pagination import paginate_page_with_limit
from api.models import Department, Experience, Vacancy


class VacanciesSortBy(Enum):
    NAME_ASC = "name_asc"
    PUBLISHED_AT_DESC = "published_at_desc"
    SALARY_ASC = "salary_asc"
    SALARY_DESC = "salary_desc"


class VacanciesWishlistSortBy(Enum):
    PUBLISHED_AT_ASC = "published_at_asc"
    ADDED_AT_DESC = "added_at_desc"


class VacanciesParams(Schema):
    search: Optional[str] = None
    department_id: Optional[int] = None
    experience: Optional[Experience] = None
    salary_from: Optional[int] = Field(None, gte=0)
    salary_to: Optional[int] = Field(None, gte=0)
    published: Optional[bool] = None
    sort_by: VacanciesSortBy
    limit: int = Field(settings.PAGINATION_PER_PAGE, ge=1)
    offset: int = Field(0, ge=0)


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
    description: Optional[str]
    leader: DepartmentLeaderOut

    @staticmethod
    def from_department(department: Department) -> "VacancyDepartmentOut":
        leader = department.leader

        return VacancyDepartmentOut(
            id=department.id,
            name=department.name,
            description=department.description,
            leader=DepartmentLeaderOut(
                id=leader.id, surname=leader.surname, name=leader.name, patronymic=leader.patronymic
            ),
        )


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

        return VacancyOut(
            id=vacancy.id,
            name=vacancy.name,
            description=vacancy.description,
            expected_experience=vacancy.expected_experience,
            salary_from=vacancy.salary_from,
            salary_to=vacancy.salary_to,
            department=VacancyDepartmentOut.from_department(vacancy.department),
            published_at=vacancy.published_at,
        )


class VacanciesOut(Schema):
    items: List[VacancyOut]
    count: int

    @staticmethod
    def from_vacancies_with_pagination(vacancies: QuerySet[Vacancy], limit: int, offset: int) -> "VacanciesOut":
        return VacanciesOut(
            items=[VacancyOut.from_vacancy(vacancy) for vacancy in paginate_page_with_limit(vacancies, offset, limit)],
            count=vacancies.count(),
        )


class VacancyIn(Schema):
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


class NewVacancyIn(VacancyIn):
    department_id: int


class PublishingOut(Schema):
    published_at: datetime

    @staticmethod
    def create(time: datetime) -> "PublishingOut":
        return PublishingOut(published_at=time)
