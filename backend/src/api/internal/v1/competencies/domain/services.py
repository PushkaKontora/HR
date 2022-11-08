from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import QuerySet

from api.internal.v1.competencies.domain.entities import CompetencyOut
from api.internal.v1.competencies.presentation.handlers import IGettingCompetenciesService
from api.models import Competency


class ICompetencyRepository(ABC):
    @abstractmethod
    def get_all(self) -> QuerySet[Competency]:
        pass


class GettingCompetenciesService(IGettingCompetenciesService):
    def __init__(self, competency_repo: ICompetencyRepository):
        self.competency_repo = competency_repo

    def get_competencies(self) -> Iterable[CompetencyOut]:
        return (CompetencyOut.from_competency(competency) for competency in self.competency_repo.get_all())
