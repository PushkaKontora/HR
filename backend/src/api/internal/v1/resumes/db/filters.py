from abc import ABC, abstractmethod
from typing import Optional, Set

from django.db.models import Q, QuerySet

from api.models import Experience, Resume


class IResumesFilter(ABC):
    @abstractmethod
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        pass


class ExperienceFilterBase(IResumesFilter, ABC):
    def __init__(self, experience: Optional[Experience]):
        self.experience = experience

    @abstractmethod
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        pass


class ExperienceFilter(ExperienceFilterBase):
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        return resumes.filter(experience=self.experience) if self.experience else resumes


class SalaryFilterBase(IResumesFilter, ABC):
    def __init__(self, salary_from: Optional[int], salary_to: Optional[int]):
        self.salary_from = salary_from
        self.salary_to = salary_to

    @abstractmethod
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        pass


class SalaryFilter(SalaryFilterBase):
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        if self.salary_from is not None:
            resumes = resumes.filter(desired_salary__gte=self.salary_from)

        if self.salary_to is not None:
            resumes = resumes.filter(desired_salary__lte=self.salary_to)

        return resumes


class CompetenciesFilterBase(IResumesFilter, ABC):
    def __init__(self, competencies_names: Optional[Set[str]]):
        self.competencies_names = competencies_names

    @abstractmethod
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        pass


class CompetenciesFilter(CompetenciesFilterBase):
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        if not self.competencies_names:
            return resumes

        return resumes.filter(competencies__in=self.competencies_names).distinct()


class PublishedFilterBase(IResumesFilter, ABC):
    def __init__(self, published: Optional[bool]):
        self.published = published

    @abstractmethod
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        pass


class PublishedFilter(PublishedFilterBase):
    def filter(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        if self.published is None:
            return resumes

        return resumes.filter(~Q(published_at=None) if self.published else Q(published_at=None))
