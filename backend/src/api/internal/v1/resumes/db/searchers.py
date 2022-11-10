from abc import ABC, abstractmethod
from typing import Optional

from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import QuerySet

from api.models import Resume


class ResumesSearcherBase(ABC):
    def __init__(self, value: Optional[str]):
        self.value = value

    @abstractmethod
    def search(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        pass


class DesiredJobSearcher(ResumesSearcherBase):
    def search(self, resumes: QuerySet[Resume]) -> QuerySet[Resume]:
        if self.value is None:
            return resumes

        return resumes.annotate(similarity=TrigramWordSimilarity(self.value, "desired_job")).filter(similarity__gte=0.5)
