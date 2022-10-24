from abc import ABC, abstractmethod
from typing import Iterable, List

from django.http import HttpRequest
from ninja import Query, Router

from api.internal.v1.competencies.domain.entities import CompetenciesFilters, CompetencyOut

COMPETENCIES_TAG = "competencies"


class ICompetenciesHandlers(ABC):
    @abstractmethod
    def get_competencies(
        self, request: HttpRequest, filters: CompetenciesFilters = Query(...)
    ) -> Iterable[CompetencyOut]:
        pass


class CompetenciesRouter(Router):
    def __init__(self, competencies_handlers: ICompetenciesHandlers):
        super(CompetenciesRouter, self).__init__(tags=[COMPETENCIES_TAG])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=competencies_handlers.get_competencies,
            response={200: List[CompetencyOut]},
        )
