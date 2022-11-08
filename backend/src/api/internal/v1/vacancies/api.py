from typing import Type

from dependency_injector import containers, providers
from ninja import NinjaAPI
from ninja.security import HttpBearer

from api.internal.v1.errors import APIBaseError
from api.internal.v1.users.api import UsersContainer
from api.internal.v1.vacancies.db.filters import DepartmentFilter, ExperienceFilter, PublishedFilter, SalaryFilter
from api.internal.v1.vacancies.db.repositories import (
    DepartmentRepository,
    FavouriteVacancyRepository,
    VacancyRepository,
)
from api.internal.v1.vacancies.db.searchers import VacanciesTrigramSearcher
from api.internal.v1.vacancies.db.sorters import (
    VacanciesSortByAverageSalaryASC,
    VacanciesSortByAverageSalaryDESC,
    VacanciesSortByNameASC,
    VacanciesSortByPublishedAtDESC,
    VacanciesSortBySalaryAtEndsASC,
    VacanciesSortBySalaryAtEndsDESC,
    VacanciesWishlistSortByAddedAtDESC,
    VacanciesWishlistSortByPublishedAtASC,
)
from api.internal.v1.vacancies.domain.builders import (
    VacanciesFiltersBuilder,
    VacanciesSearcherBuilder,
    VacanciesSorterBuilder,
)
from api.internal.v1.vacancies.domain.services import (
    CreatingVacancyService,
    GettingVacanciesService,
    GettingVacancyService,
    PublishingVacancyService,
    UpdatingVacancyService,
    VacanciesWishlistService,
)
from api.internal.v1.vacancies.presentation.errors import (
    UnknownDepartmentIdError,
    VacancyAlreadyAddedToWishlistError,
    YouCannotAddUnpublishedVacancyToWishlistError,
)
from api.internal.v1.vacancies.presentation.handlers import (
    VacanciesHandlers,
    VacanciesWishlistHandlers,
    VacancyHandlers,
)
from api.internal.v1.vacancies.presentation.routers import VacanciesRouter, VacanciesWishlistRouter, VacancyRouter

ERRORS = [UnknownDepartmentIdError, YouCannotAddUnpublishedVacancyToWishlistError, VacancyAlreadyAddedToWishlistError]


class VacanciesContainer(containers.DeclarativeContainer):
    auth = providers.ExternalDependency(HttpBearer)

    vacancy_repo = providers.Singleton(VacancyRepository)
    department_repo = providers.Singleton(DepartmentRepository)
    favourite_vacancy_repo = providers.Singleton(FavouriteVacancyRepository)

    creating_vacancy_service = providers.Singleton(
        CreatingVacancyService, vacancy_repo=vacancy_repo, department_repo=department_repo
    )
    getting_vacancy_service = providers.Singleton(GettingVacancyService, vacancy_repo=vacancy_repo)
    publishing_vacancy_service = providers.Singleton(
        PublishingVacancyService, vacancy_repo=vacancy_repo, favourite_vacancy_repo=favourite_vacancy_repo
    )
    vacancies_wishlist_service = providers.Singleton(
        VacanciesWishlistService,
        favourite_vacancy_repo=favourite_vacancy_repo,
        published_at_asc_sorter=providers.Factory(VacanciesWishlistSortByPublishedAtASC),
        added_at_desc_sorter=providers.Factory(VacanciesWishlistSortByAddedAtDESC),
    )
    updating_vacancy_service = providers.Singleton(UpdatingVacancyService, vacancy_repo=vacancy_repo)

    getting_vacancies_service = providers.Singleton(
        GettingVacanciesService,
        vacancy_repo=vacancy_repo,
        vacancies_filters_builder=providers.Singleton(
            VacanciesFiltersBuilder,
            department_filter_cls=providers.Object(DepartmentFilter),
            experience_filter_cls=providers.Object(ExperienceFilter),
            salary_filter_cls=providers.Object(SalaryFilter),
            published_filter_cls=providers.Object(PublishedFilter),
        ),
        searcher_builder=providers.Singleton(
            VacanciesSearcherBuilder, searcher_cls=providers.Object(VacanciesTrigramSearcher)
        ),
        sorter_builder=providers.Singleton(
            VacanciesSorterBuilder,
            name_asc_sorter_cls=providers.Object(VacanciesSortByNameASC),
            published_at_desc_sorter_cls=providers.Object(VacanciesSortByPublishedAtDESC),
            salary_asc_sorter_cls=providers.Object(VacanciesSortByAverageSalaryASC),
            salary_desc_sorter_cls=providers.Object(VacanciesSortByAverageSalaryDESC),
        ),
    )

    vacancies_wishlist_handlers = providers.Singleton(
        VacanciesWishlistHandlers,
        vacancies_wishlist_service=vacancies_wishlist_service,
        getting_vacancy_service=getting_vacancy_service,
    )
    vacancy_handlers = providers.Singleton(
        VacancyHandlers,
        getting_vacancy_service=getting_vacancy_service,
        publishing_vacancy_service=publishing_vacancy_service,
        updating_vacancy_service=updating_vacancy_service,
    )
    vacancies_handlers = providers.Singleton(
        VacanciesHandlers,
        creating_vacancy_service=creating_vacancy_service,
        getting_vacancy_service=getting_vacancy_service,
        getting_vacancies_service=getting_vacancies_service,
    )

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
