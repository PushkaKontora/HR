from abc import ABC, abstractmethod
from typing import Optional

from django.db.models import Q, QuerySet

from api.models import Experience, Vacancy


class IVacanciesFilter(ABC):
    @abstractmethod
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass


class SalaryBaseFilter(IVacanciesFilter, ABC):
    def __init__(self, salary_from: Optional[int], salary_to: Optional[int]):
        self.salary_to = salary_to
        self.salary_from = salary_from

    @abstractmethod
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass


class DepartmentBaseFilter(IVacanciesFilter, ABC):
    def __init__(self, department_id: Optional[int]):
        self.department_id = department_id

    @abstractmethod
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass


class ExperienceBaseFilter(IVacanciesFilter, ABC):
    def __init__(self, experience: Optional[Experience]):
        self.experience = experience

    @abstractmethod
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass


class PublishedBaseFilter(IVacanciesFilter, ABC):
    def __init__(self, published: Optional[bool]):
        self.published = published

    @abstractmethod
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass


class DepartmentFilter(DepartmentBaseFilter):
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return vacancies if self.department_id is None else vacancies.filter(department_id=self.department_id)


class ExperienceFilter(ExperienceBaseFilter):
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return vacancies if self.experience is None else vacancies.filter(expected_experience=self.experience)


class SalaryFilter(SalaryBaseFilter):
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        if self.salary_from is not None:
            vacancies = vacancies.filter(salary_from__gte=self.salary_from)

        if self.salary_to is not None:
            vacancies = vacancies.filter(salary_to__lte=self.salary_to)

        return vacancies


class PublishedFilter(PublishedBaseFilter):
    def filter(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        if self.published is None:
            return vacancies

        return vacancies.filter(~Q(published_at=None) if self.published else Q(published_at=None))
