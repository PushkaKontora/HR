from abc import ABC, abstractmethod
from typing import Iterable

from django.http import HttpRequest
from ninja import Body, Path, Query
from ninja.pagination import LimitOffsetPagination, paginate

from api.internal.v1.exceptions import ForbiddenError
from api.internal.v1.responses import SuccessResponse
from api.internal.v1.vacancies.domain.entities import (
    PublishingOut,
    RequestOut,
    VacanciesFilters,
    VacanciesWishlistFilters,
    VacanciesWishlistIn,
    VacancyIn,
    VacancyOut,
)
from api.internal.v1.vacancies.presentation.errors import UnknownDepartmentIdError
from api.internal.v1.vacancies.presentation.routers import (
    IVacanciesHandlers,
    IVacanciesWishlistHandlers,
    IVacancyHandlers,
)
from api.models import User


class ICreatingVacancyService(ABC):
    @abstractmethod
    def exists_department_with_id(self, department_id: int) -> bool:
        pass

    @abstractmethod
    def authorize(self, auth_user: User, body: VacancyIn) -> bool:
        pass

    @abstractmethod
    def create(self, body: VacancyIn) -> None:
        pass


class VacanciesHandlers(IVacanciesHandlers):
    def __init__(self, creating_vacancy_service: ICreatingVacancyService):
        self.creating_vacancy_service = creating_vacancy_service

    def create_vacancy(self, request: HttpRequest, body: VacancyIn = Body(...)) -> SuccessResponse:
        if not self.creating_vacancy_service.exists_department_with_id(body.department_id):
            raise UnknownDepartmentIdError()

        if not self.creating_vacancy_service.authorize(request.user, body):
            raise ForbiddenError()

        self.creating_vacancy_service.create(body)

        return SuccessResponse()

    @paginate(LimitOffsetPagination)
    def get_vacancies(self, request: HttpRequest, filters: VacanciesFilters = Query(...)) -> Iterable[VacancyOut]:
        raise NotImplementedError()


class VacancyHandlers(IVacancyHandlers):
    def get_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> VacancyOut:
        raise NotImplementedError()

    def update_vacancy(
        self, request: HttpRequest, vacancy_id: int = Path(...), body: VacancyIn = Body(...)
    ) -> SuccessResponse:
        raise NotImplementedError()

    def create_vacancy_request(self, request: HttpRequest, vacancy_id: int = Path(...)) -> RequestOut:
        raise NotImplementedError()

    def publish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> PublishingOut:
        raise NotImplementedError()

    def unpublish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        raise NotImplementedError()

    def get_vacancy_request(self, request: HttpRequest, vacancy_id: int = Path(...)) -> RequestOut:
        raise NotImplementedError()


class VacanciesWishlistHandlers(IVacanciesWishlistHandlers):
    def get_vacancies_wishlist(
        self, request: HttpRequest, filters: VacanciesWishlistFilters = Query(...)
    ) -> Iterable[VacancyOut]:
        raise NotImplementedError()

    def add_vacancy_to_wishlist(self, request: HttpRequest, body: VacanciesWishlistIn = Body(...)) -> SuccessResponse:
        raise NotImplementedError()
