from typing import Type

from dependency_injector import containers, providers
from ninja import NinjaAPI
from ninja.security import HttpBearer

from api.internal.v1.exceptions import APIBaseError
from api.internal.v1.users.api import UsersContainer
from api.internal.v1.vacancies.db.repositories import DepartmentRepository, VacancyRepository
from api.internal.v1.vacancies.domain.services import CreatingVacancyService
from api.internal.v1.vacancies.presentation.errors import UnknownDepartmentIdError
from api.internal.v1.vacancies.presentation.handlers import (
    VacanciesHandlers,
    VacanciesWishlistHandlers,
    VacancyHandlers,
)
from api.internal.v1.vacancies.presentation.routers import VacanciesRouter, VacanciesWishlistRouter, VacancyRouter

ERRORS = [UnknownDepartmentIdError]


class VacanciesContainer(containers.DeclarativeContainer):
    auth = providers.ExternalDependency(HttpBearer)

    vacancy_repo = providers.Singleton(VacancyRepository)
    department_repo = providers.Singleton(DepartmentRepository)

    creating_vacancy_service = providers.Singleton(
        CreatingVacancyService, vacancy_repo=vacancy_repo, department_repo=department_repo
    )

    vacancies_wishlist_handlers = providers.Singleton(VacanciesWishlistHandlers)
    vacancy_handlers = providers.Singleton(VacancyHandlers)
    vacancies_handlers = providers.Singleton(VacanciesHandlers, creating_vacancy_service=creating_vacancy_service)

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

    for error in ERRORS:
        base.add_exception_handler(error, _get_handler(error))

    base.add_router("/vacancies", container.vacancies_router())


def _get_handler(error: Type[APIBaseError]):
    return lambda request, exc: error.response(exc)
