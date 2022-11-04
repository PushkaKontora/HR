from abc import ABC, abstractmethod
from typing import Any, Set

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramWordSimilarity
from django.db.models import QuerySet

from api.models import Experience, Resume


class IResumesSearcher(ABC):
    @abstractmethod
    def search(self, resumes: QuerySet[Resume], value: Any) -> QuerySet[Resume]:
        pass


class DesiredJobSearcher(IResumesSearcher):
    def search(self, resumes: QuerySet[Resume], value: str) -> QuerySet[Resume]:
        return (
            resumes.annotate(similarity=TrigramWordSimilarity(value, "desired_job"))
            .filter(similarity__gte=0.3)
            .order_by("-similarity")
        )


class ExperienceSearcher(IResumesSearcher):
    def search(self, resumes: QuerySet[Resume], value: Experience) -> QuerySet[Resume]:
        return resumes.filter(experience=value)


class SalaryFromSearcher(IResumesSearcher):
    def search(self, resumes: QuerySet[Resume], value: int) -> QuerySet[Resume]:
        return resumes.filter(desired_salary__gte=value)


class SalaryToSearcher(IResumesSearcher):
    def search(self, resumes: QuerySet[Resume], value: int) -> QuerySet[Resume]:
        return resumes.filter(desired_salary__lte=value)


class CompetenciesSearcher(IResumesSearcher):
    def search(self, resumes: QuerySet[Resume], value: Set[str]) -> QuerySet[Resume]:
        return resumes.filter(competencies__in=value).distinct()
