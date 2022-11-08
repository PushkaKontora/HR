from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.v1.competencies.db.repositories import CompetencyRepository
from api.internal.v1.competencies.domain.services import GettingCompetenciesService
from api.internal.v1.competencies.presentation.handlers import CompetenciesHandlers
from api.internal.v1.competencies.presentation.routers import CompetenciesRouter


class CompetenciesContainer(containers.DeclarativeContainer):
    competency_repo = providers.Singleton(CompetencyRepository)

    getting_competencies_service = providers.Singleton(GettingCompetenciesService, competency_repo=competency_repo)

    competencies_handlers = providers.Singleton(
        CompetenciesHandlers, getting_competencies_service=getting_competencies_service
    )

    competencies_router = providers.Singleton(CompetenciesRouter, competencies_handlers=competencies_handlers)


def register_competencies_api(base: NinjaAPI) -> None:
    container = CompetenciesContainer()

    base.add_router("/competencies", container.competencies_router())
