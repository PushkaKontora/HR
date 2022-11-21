from abc import ABC, abstractmethod
from typing import Optional

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramWordSimilarity
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

        return vacancies.annotate(
            similarity=Greatest(
                TrigramWordSimilarity(self.value, "name"), TrigramWordSimilarity(self.value, "description")
            )
        ).filter(similarity__gte=0.5)


class VacanciesCombineSearcher(VacanciesBaseSearcher):
    def search(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        if self.value is None:
            return vacancies

        return self.get_full_text_queryset(vacancies) or self.get_trigram_queryset(vacancies)

    def get_full_text_queryset(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        query = SearchQuery(self.value)
        vector = SearchVector("name", weight="A") + SearchVector("description", weight="B")

        return vacancies.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.5)

    def get_trigram_queryset(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return vacancies.annotate(
            similarity=Greatest(
                TrigramWordSimilarity(self.value, "name"), TrigramWordSimilarity(self.value, "description")
            )
        ).filter(similarity__gte=0.5)
