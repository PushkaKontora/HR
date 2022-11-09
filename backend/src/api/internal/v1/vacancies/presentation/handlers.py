from abc import ABC, abstractmethod
from typing import Iterable, Optional

from django.http import HttpRequest
from ninja import Body, Path, Query
from ninja.pagination import LimitOffsetPagination, paginate

from api.internal.v1.errors import ForbiddenError, NotFoundError
from api.internal.v1.responses import SuccessResponse
from api.internal.v1.vacancies.domain.entities import (
    NewVacancyIn,
    PublishingOut,
    VacanciesFilters,
    VacanciesWishlistParams,
    VacancyIn,
    VacancyOut,
)
from api.internal.v1.vacancies.presentation.errors import (
    UnknownDepartmentIdError,
    VacancyAlreadyAddedToWishlistError,
    YouCannotAddUnpublishedVacancyToWishlistError,
)
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
    def authorize(self, auth_user: User, body: NewVacancyIn) -> bool:
        pass

    @abstractmethod
    def create(self, body: NewVacancyIn) -> None:
        pass


class IGettingService(ABC):
    @abstractmethod
    def try_get_vacancy_out_by_id(self, vacancy_id: int) -> Optional[VacancyOut]:
        pass

    @abstractmethod
    def exists_vacancy_with_id(self, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def is_published(self, vacancy_id: int) -> bool:
        pass


class IPublishingVacancyService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def publish(self, vacancy_id: int) -> PublishingOut:
        pass

    @abstractmethod
    def unpublish(self, vacancy_id: int) -> None:
        pass


class IVacanciesWishlistService(ABC):
    @abstractmethod
    def get_user_wishlist(self, auth_user: User, params: VacanciesWishlistParams) -> Iterable[VacancyOut]:
        pass

    @abstractmethod
    def exists_vacancy_in_wishlist(self, auth_user: User, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def add_vacancy_to_wishlist(self, auth_user: User, vacancy_id: int) -> None:
        pass

    @abstractmethod
    def delete_vacancy_from_wishlist(self, auth_user: User, vacancy_id: int) -> None:
        pass


class IUpdatingVacancyService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def update_vacancy(self, vacancy_id: int, body: VacancyIn) -> None:
        pass


class VacanciesHandlers(IVacanciesHandlers):
    def __init__(self, creating_vacancy_service: ICreatingVacancyService):
        self.creating_vacancy_service = creating_vacancy_service

    def create_vacancy(self, request: HttpRequest, body: NewVacancyIn = Body(...)) -> SuccessResponse:
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
    def __init__(
        self,
        getting_service: IGettingService,
        publishing_vacancy_service: IPublishingVacancyService,
        updating_vacancy_service: IUpdatingVacancyService,
    ):
        self.updating_vacancy_service = updating_vacancy_service
        self.publishing_vacancy_service = publishing_vacancy_service
        self.getting_service = getting_service

    def get_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> VacancyOut:
        vacancy_out = self.getting_service.try_get_vacancy_out_by_id(vacancy_id)

        if not vacancy_out:
            raise NotFoundError()

        return vacancy_out

    def update_vacancy(
        self, request: HttpRequest, vacancy_id: int = Path(...), body: VacancyIn = Body(...)
    ) -> SuccessResponse:
        if not self.getting_service.exists_vacancy_with_id(vacancy_id):
            raise NotFoundError()

        if not self.updating_vacancy_service.authorize(request.user, vacancy_id):
            raise ForbiddenError()

        self.updating_vacancy_service.update_vacancy(vacancy_id, body)

        return SuccessResponse()

    def publish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> PublishingOut:
        if not self.getting_service.exists_vacancy_with_id(vacancy_id):
            raise NotFoundError()

        if not self.publishing_vacancy_service.authorize(request.user, vacancy_id):
            raise ForbiddenError()

        return self.publishing_vacancy_service.publish(vacancy_id)

    def unpublish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        if not self.getting_service.exists_vacancy_with_id(vacancy_id):
            raise NotFoundError()

        if not self.publishing_vacancy_service.authorize(request.user, vacancy_id):
            raise ForbiddenError()

        self.publishing_vacancy_service.unpublish(vacancy_id)

        return SuccessResponse()


class VacanciesWishlistHandlers(IVacanciesWishlistHandlers):
    def __init__(self, vacancies_wishlist_service: IVacanciesWishlistService, getting_service: IGettingService):
        self.getting_service = getting_service
        self.vacancies_wishlist_service = vacancies_wishlist_service

    def get_vacancies_wishlist(
        self, request: HttpRequest, params: VacanciesWishlistParams = Query(...)
    ) -> Iterable[VacancyOut]:
        return self.vacancies_wishlist_service.get_user_wishlist(request.user, params)

    def add_vacancy_to_wishlist(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        if not self.getting_service.exists_vacancy_with_id(vacancy_id):
            raise NotFoundError()

        if not self.getting_service.is_published(vacancy_id):
            raise YouCannotAddUnpublishedVacancyToWishlistError()

        if self.vacancies_wishlist_service.exists_vacancy_in_wishlist(request.user, vacancy_id):
            raise VacancyAlreadyAddedToWishlistError()

        self.vacancies_wishlist_service.add_vacancy_to_wishlist(request.user, vacancy_id)

        return SuccessResponse()

    def delete_vacancy_from_wishlist(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        if not self.vacancies_wishlist_service.exists_vacancy_in_wishlist(request.user, vacancy_id):
            raise NotFoundError()

        self.vacancies_wishlist_service.delete_vacancy_from_wishlist(request.user, vacancy_id)

        return SuccessResponse()
