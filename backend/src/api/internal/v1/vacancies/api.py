from dependency_injector import containers, providers
from ninja import NinjaAPI
from ninja.security import HttpBearer

from api.internal.v1.users.api import UsersContainer
from api.internal.v1.vacancies.presentation.handlers import (
    VacanciesHandlers,
    VacanciesWishlistHandlers,
    VacancyHandlers,
)
from api.internal.v1.vacancies.presentation.routers import VacanciesRouter, VacanciesWishlistRouter, VacancyRouter


class VacanciesContainer(containers.DeclarativeContainer):
    auth = providers.ExternalDependency(HttpBearer)

    vacancies_wishlist_handlers = providers.Singleton(VacanciesWishlistHandlers)
    vacancy_handlers = providers.Singleton(VacancyHandlers)
    vacancies_handlers = providers.Singleton(VacanciesHandlers)

    vacancies_wishlist_router = providers.Singleton(
        VacanciesWishlistRouter, vacancies_wishlist_handlers=vacancies_wishlist_handlers, auth=auth
    )
    vacancy_router = providers.Singleton(
        VacancyRouter,
        vacancy_handlers=vacancy_handlers,
        auth=auth,
    )
    vacancies_router = providers.Singleton(
        VacanciesRouter,
        vacancy_router=vacancy_router,
        vacancies_wishlist_router=vacancies_wishlist_router,
        vacancies_handlers=vacancies_handlers,
        auth=auth,
    )


def register_vacancies_api(base: NinjaAPI) -> None:
    container = VacanciesContainer(auth=UsersContainer().auth())

    base.add_router("/vacancies", container.vacancies_router())
