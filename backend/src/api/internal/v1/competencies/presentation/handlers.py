from typing import Iterable

from django.http import HttpRequest
from ninja import Query

from api.internal.v1.competencies.domain.entities import CompetenciesFilters, CompetencyOut
from api.internal.v1.competencies.presentation.routers import ICompetenciesHandlers


class CompetenciesHandlers(ICompetenciesHandlers):
    def get_competencies(
        self, request: HttpRequest, filters: CompetenciesFilters = Query(...)
    ) -> Iterable[CompetencyOut]:
        raise NotImplementedError()
