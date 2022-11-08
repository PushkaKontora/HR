from abc import ABC, abstractmethod
from typing import Optional

from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import QuerySet
from django.db.models.functions import Greatest

from api.models import Vacancy


class VacanciesBaseSearcher(ABC):
    def __init__(self, value: Optional[str]):
        self.value = value

    @abstractmethod
    def search(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass


class VacanciesTrigramSearcher(VacanciesBaseSearcher):
    def search(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        if self.value is None:
            return vacancies

        return (
            vacancies.annotate(
                similarity=TrigramWordSimilarity(self.value, "name") + TrigramWordSimilarity(self.value, "description")
            )
            .filter(similarity__gte=0.3)
            .order_by("-similarity")
        )
