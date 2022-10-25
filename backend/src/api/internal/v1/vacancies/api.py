from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.authentication import JWTBaseAuthentication
from api.internal.models import User
from api.internal.v1.vacancies.presentation.handlers import (
    VacanciesHandlers,
    VacanciesWishlistHandlers,
    VacancyHandlers,
)
from api.internal.v1.vacancies.presentation.routers import VacanciesRouter, VacanciesWishlistRouter, VacancyRouter


class AnyUserStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class OnlyEmployerStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class Container(containers.DeclarativeContainer):
    any_user = providers.Factory(AnyUserStub)
    only_employer = providers.Factory(OnlyEmployerStub)

    vacancies_wishlist_handlers = providers.Singleton(VacanciesWishlistHandlers)
    vacancy_handlers = providers.Singleton(VacancyHandlers)
    vacancies_handlers = providers.Singleton(VacanciesHandlers)

    vacancies_wishlist_router = providers.Singleton(
        VacanciesWishlistRouter, vacancies_wishlist_handlers=vacancies_wishlist_handlers, any_user=any_user
    )
    vacancy_router = providers.Singleton(
        VacancyRouter,
        vacancy_handlers=vacancy_handlers,
        any_user=any_user,
        only_employer=only_employer,
    )
    vacancies_router = providers.Singleton(
        VacanciesRouter,
        vacancy_router=vacancy_router,
        vacancies_wishlist_router=vacancies_wishlist_router,
        vacancies_handlers=vacancies_handlers,
        only_employer=only_employer
    )


def register_vacancies_api(base: NinjaAPI) -> None:
    container = Container()

    base.add_router("/vacancies", container.vacancies_router())
