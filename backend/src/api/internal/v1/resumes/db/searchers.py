from abc import ABC, abstractmethod
from typing import Optional

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramWordSimilarity
from django.db.models import QuerySet

from api.models import Resume


class ResumesSearcherBase(ABC):
    def __init__(self, value: Optional[str]):
        self.value = value

    @abstractmethod
    def search(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        pass


class DesiredJobTrigramSearcher(ResumesSearcherBase):
    def search(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        if self.value is None:
            return resumes

        return resumes.annotate(similarity=TrigramWordSimilarity(self.value, "desired_job")).filter(similarity__gte=0.5)


class ResumesCombineSearcher(ResumesSearcherBase):
    def search(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        if self.value is None:
            return resumes

        return self.get_full_text_queryset(resumes) or self.get_trigram_queryset(resumes)

    def get_full_text_queryset(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        query = SearchQuery(self.value)
        vector = SearchVector("desired_job")

        return resumes.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.5)

    def get_trigram_queryset(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        return resumes.annotate(similarity=TrigramWordSimilarity(self.value, "desired_job")).filter(similarity__gte=0.5)
