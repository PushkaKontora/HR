from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.v1.competencies.presentation.handlers import CompetenciesHandlers
from api.internal.v1.competencies.presentation.routers import CompetenciesRouter


class Container(containers.DeclarativeContainer):
    competencies_handlers = providers.Singleton(CompetenciesHandlers)

    competencies_router = providers.Singleton(CompetenciesRouter, competencies_handlers=competencies_handlers)


def register_competencies_api(base: NinjaAPI) -> None:
    container = Container()

    base.add_router("/competencies", container.competencies_router())
