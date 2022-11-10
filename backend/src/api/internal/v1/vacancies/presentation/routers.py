from abc import ABC, abstractmethod
from typing import Iterable, List

from django.http import HttpRequest
from ninja import Body, Path, Query, Router
from ninja.security import HttpBearer

from api.internal.v1.responses import ErrorResponse, MessageResponse, SuccessResponse
from api.internal.v1.vacancies.domain.entities import (
    NewVacancyIn,
    PublishingOut,
    VacanciesOut,
    VacanciesParams,
    VacanciesWishlistParams,
    VacancyIn,
    VacancyOut,
)

VACANCIES_TAG = "vacancies"


class IVacanciesHandlers(ABC):
    @abstractmethod
    def get_vacancies(self, request: HttpRequest, params: VacanciesParams = Query(...)) -> VacanciesOut:
        pass

    @abstractmethod
    def create_vacancy(self, request: HttpRequest, body: NewVacancyIn = Body(...)) -> SuccessResponse:
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
    def publish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> PublishingOut:
        pass

    @abstractmethod
    def unpublish_vacancy(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        pass


class IVacanciesWishlistHandlers(ABC):
    @abstractmethod
    def get_vacancies_wishlist(
        self, request: HttpRequest, params: VacanciesWishlistParams = Query(...)
    ) -> Iterable[VacancyOut]:
        pass

    @abstractmethod
    def add_vacancy_to_wishlist(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def delete_vacancy_from_wishlist(self, request: HttpRequest, vacancy_id: int = Path(...)) -> SuccessResponse:
        pass


class VacanciesRouter(Router):
    def __init__(
        self,
        vacancy_router: Router,
        vacancies_wishlist_router: Router,
        vacancies_handlers: IVacanciesHandlers,
        auth: HttpBearer,
    ):
        super(VacanciesRouter, self).__init__(tags=[VACANCIES_TAG])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=vacancies_handlers.get_vacancies,
            response={200: VacanciesOut},
        )

        self.add_api_operation(
            path="",
            methods=["POST"],
            view_func=vacancies_handlers.create_vacancy,
            auth=[auth],
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 422: ErrorResponse},
        )

        self.add_router("/{int:vacancy_id}", vacancy_router)
        self.add_router("/wishlist", vacancies_wishlist_router)


class VacancyRouter(Router):
    def __init__(self, vacancy_handlers: IVacancyHandlers, auth: HttpBearer):
        super(VacancyRouter, self).__init__(tags=[VACANCIES_TAG])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=vacancy_handlers.get_vacancy,
            response={200: VacancyOut, 404: MessageResponse},
        )

        self.add_api_operation(
            path="",
            methods=["PUT"],
            view_func=vacancy_handlers.update_vacancy,
            auth=[auth],
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
        )

        self.add_api_operation(
            path="/publish",
            methods=["PATCH"],
            view_func=vacancy_handlers.publish_vacancy,
            auth=[auth],
            response={200: PublishingOut, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
        )

        self.add_api_operation(
            path="/unpublish",
            methods=["PATCH"],
            view_func=vacancy_handlers.unpublish_vacancy,
            auth=[auth],
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
        )


class VacanciesWishlistRouter(Router):
    def __init__(self, vacancies_wishlist_handlers: IVacanciesWishlistHandlers, auth: HttpBearer):
        super(VacanciesWishlistRouter, self).__init__(tags=[VACANCIES_TAG], auth=[auth])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=vacancies_wishlist_handlers.get_vacancies_wishlist,
            response={200: List[VacancyOut], 401: MessageResponse},
        )

        self.add_api_operation(
            path="/{int:vacancy_id}",
            methods=["POST"],
            view_func=vacancies_wishlist_handlers.add_vacancy_to_wishlist,
            response={200: SuccessResponse, 401: MessageResponse, 404: MessageResponse, 422: ErrorResponse},
        )

        self.add_api_operation(
            path="/{int:vacancy_id}",
            methods=["DELETE"],
            view_func=vacancies_wishlist_handlers.delete_vacancy_from_wishlist,
            response={200: SuccessResponse, 401: MessageResponse, 404: MessageResponse},
        )
