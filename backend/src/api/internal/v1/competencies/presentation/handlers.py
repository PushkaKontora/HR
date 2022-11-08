from abc import ABC, abstractmethod
from typing import Iterable

from django.http import HttpRequest

from api.internal.v1.competencies.domain.entities import CompetencyOut
from api.internal.v1.competencies.presentation.routers import ICompetenciesHandlers


class IGettingCompetenciesService(ABC):
    @abstractmethod
    def get_competencies(self) -> Iterable[CompetencyOut]:
        pass


class CompetenciesHandlers(ICompetenciesHandlers):
    def __init__(self, getting_competencies_service: IGettingCompetenciesService):
        self.getting_competencies_service = getting_competencies_service

    def get_competencies(self, request: HttpRequest) -> Iterable[CompetencyOut]:
        return self.getting_competencies_service.get_competencies()
