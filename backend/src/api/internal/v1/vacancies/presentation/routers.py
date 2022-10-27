from abc import ABC, abstractmethod
from typing import Iterable, List

from django.http import HttpRequest
from ninja import Body, Path, Query, Router

from api.internal.authentication import JWTBaseAuthentication
from api.internal.base import NOT_IMPLEMENTED_TAG, ErrorResponse, SuccessResponse
from api.internal.v1.vacancies.domain.entities import (
    PublishingOut,
    RequestOut,
    VacanciesFilters,
    VacanciesWishlistFilters,
    VacanciesWishlistIn,
    VacancyIn,
    VacancyOut,
)

VACANCIES_TAG = "vacancies"


class IVacanciesHandlers(ABC):
    @abstractmethod
    def get_vacancies(self, request: HttpRequest, filters: VacanciesFilters = Query(...)) -> Iterable[VacancyOut]:
        pass

    @abstractmethod
    def create_vacancy(self, request: HttpRequest, body: VacancyIn = Body(...)) -> SuccessResponse:
        pass


class IVacancyHandlers(ABC):
    @abstractmethod
    def get_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> VacancyOut:
        pass

    @abstractmethod
    def update_vacancy(
        self, request: HttpRequest, vacancy_id: int = Path(...), body: VacancyIn = Body(...)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def create_vacancy_request(self, request: HttpRequest, vacancy_id: int = Path(...)) -> RequestOut:
        pass

    @abstractmethod
    def publish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> PublishingOut:
        pass

    @abstractmethod
    def unpublish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def get_vacancy_request(self, request: HttpRequest, vacancy_id: int = Path(...)) -> RequestOut:
        pass


class IVacanciesWishlistHandlers(ABC):
    @abstractmethod
    def get_vacancies_wishlist(
        self, request: HttpRequest, filters: VacanciesWishlistFilters = Query(...)
    ) -> Iterable[VacancyOut]:
        pass

    @abstractmethod
    def add_vacancy_to_wishlist(self, request: HttpRequest, body: VacanciesWishlistIn = Body(...)) -> SuccessResponse:
        pass


class VacanciesRouter(Router):
    def __init__(
        self,
        vacancy_router: Router,
        vacancies_wishlist_router: Router,
        vacancies_handlers: IVacanciesHandlers,
        only_employer: JWTBaseAuthentication,
    ):
        super(VacanciesRouter, self).__init__(tags=[VACANCIES_TAG])

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["GET"],
            view_func=vacancies_handlers.get_vacancies,
            response={200: List[VacancyOut]},
        )

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["POST"],
            view_func=vacancies_handlers.create_vacancy,
            auth=[only_employer],
            response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 422: ErrorResponse},
        )

        self.add_router("/{int:vacancy_id}", vacancy_router)
        self.add_router("/wishlist", vacancies_wishlist_router)


class VacancyRouter(Router):
    def __init__(
        self, vacancy_handlers: IVacancyHandlers, any_user: JWTBaseAuthentication, only_employer: JWTBaseAuthentication
    ):
        super(VacancyRouter, self).__init__(tags=[VACANCIES_TAG])

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["GET"],
            view_func=vacancy_handlers.get_vacancy,
            response={200: VacancyOut, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["PUT"],
            view_func=vacancy_handlers.update_vacancy,
            auth=[only_employer],
            response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="/request",
            methods=["GET"],
            view_func=vacancy_handlers.get_vacancy_request,
            auth=[any_user],
            response={200: RequestOut, 401: ErrorResponse, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="/request",
            methods=["POST"],
            view_func=vacancy_handlers.create_vacancy_request,
            auth=[any_user],
            response={200: RequestOut, 401: ErrorResponse, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="/publish",
            methods=["PATCH"],
            view_func=vacancy_handlers.publish_vacancy,
            auth=[only_employer],
            response={200: PublishingOut, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="/unpublish",
            methods=["PATCH"],
            view_func=vacancy_handlers.unpublish_vacancy,
            auth=[only_employer],
            response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse},
        )


class VacanciesWishlistRouter(Router):
    def __init__(self, vacancies_wishlist_handlers: IVacanciesWishlistHandlers, any_user: JWTBaseAuthentication):
        super(VacanciesWishlistRouter, self).__init__(tags=[VACANCIES_TAG])

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["GET"],
            view_func=vacancies_wishlist_handlers.get_vacancies_wishlist,
            auth=[any_user],
            response={200: List[VacancyOut], 401: ErrorResponse},
        )

        self.add_api_operation(
            tags=[VACANCIES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["POST"],
            view_func=vacancies_wishlist_handlers.add_vacancy_to_wishlist,
            auth=[any_user],
            response={200: SuccessResponse, 401: ErrorResponse},
        )
