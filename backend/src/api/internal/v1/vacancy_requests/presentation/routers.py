from abc import ABC, abstractmethod
from typing import Optional

from django.http import HttpRequest
from ninja import File, Form, Query, Router, UploadedFile
from ninja.security import HttpBearer

from api.internal.v1.responses import ErrorResponse, MessageResponse
from api.internal.v1.vacancy_requests.domain.entities import RequestIn, RequestOut

VACANCY_REQUEST_TAG = "vacancy requests"


class IVacancyRequestsHandlers(ABC):
    @abstractmethod
    def create_vacancy_request(
        self, request: HttpRequest, extra: RequestIn = Form(...), resume: Optional[UploadedFile] = File(None)
    ) -> RequestOut:
        pass

    @abstractmethod
    def get_last_vacancy_request(self, request: HttpRequest, vacancy_id: int = Query(...)) -> RequestOut:
        pass


class VacancyRequestsRouter(Router):
    def __init__(self, vacancy_requests_handlers: IVacancyRequestsHandlers, auth: HttpBearer):
        super(VacancyRequestsRouter, self).__init__(tags=[VACANCY_REQUEST_TAG])

        self.add_api_operation(
            path="",
            methods=["POST"],
            view_func=vacancy_requests_handlers.create_vacancy_request,
            auth=[auth],
            response={200: RequestOut, 401: MessageResponse, 404: MessageResponse, 422: ErrorResponse},
        )

        self.add_api_operation(
            path="/last",
            methods=["GET"],
            view_func=vacancy_requests_handlers.get_last_vacancy_request,
            auth=[auth],
            response={200: RequestOut, 401: MessageResponse, 404: MessageResponse},
        )
