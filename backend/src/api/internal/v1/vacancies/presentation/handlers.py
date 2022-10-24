from typing import Iterable

from django.http import HttpRequest
from ninja import Body, Path, Query

from api.internal.base import SuccessResponse
from api.internal.v1.vacancies.domain.entities import (
    PublishingOut,
    RequestOut,
    VacanciesFilters,
    VacanciesWishlistFilters,
    VacanciesWishlistIn,
    VacancyIn,
    VacancyOut,
)
from api.internal.v1.vacancies.presentation.routers import (
    IVacanciesHandlers,
    IVacanciesWishlistHandlers,
    IVacancyHandlers,
)


class VacanciesHandlers(IVacanciesHandlers):
    def get_vacancies(self, request: HttpRequest, filters: VacanciesFilters = Query(...)) -> Iterable[VacancyOut]:
        pass


class VacancyHandlers(IVacancyHandlers):
    def get_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> VacancyOut:
        pass

    def update_vacancy(
        self, request: HttpRequest, vacancy_id: int = Path(...), body: VacancyIn = Body(...)
    ) -> SuccessResponse:
        pass

    def create_vacancy_request(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        pass

    def publish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> PublishingOut:
        pass

    def unpublish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        pass

    def get_vacancy_request(self, request: HttpRequest, vacancy_id: int = Path(...)) -> RequestOut:
        pass


class VacanciesWishlistHandlers(IVacanciesWishlistHandlers):
    def get_vacancies_wishlist(
        self, request: HttpRequest, filters: VacanciesWishlistFilters = Query(...)
    ) -> Iterable[VacancyOut]:
        pass

    def add_vacancy_to_wishlist(self, request: HttpRequest, body: VacanciesWishlistIn = Body(...)) -> SuccessResponse:
        pass
