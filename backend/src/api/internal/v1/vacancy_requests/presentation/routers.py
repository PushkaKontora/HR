from abc import ABC, abstractmethod
from typing import Optional

from django.conf import settings
from django.http import HttpRequest
from ninja import File, Form, Query, Router, UploadedFile
from ninja.security import HttpBearer

from api.internal.responses import DomainErrorResponse, MessageResponse
from api.internal.v1.vacancy_requests.domain.entities import RequestIn, VacancyRequestOut

VACANCY_REQUEST_TAG = "vacancy requests"


class IVacancyRequestsHandlers(ABC):
    @abstractmethod
    def create_vacancy_request(
        self, request: HttpRequest, extra: RequestIn = Form(...), resume: Optional[UploadedFile] = File(None)
    ) -> VacancyRequestOut:
        pass

    @abstractmethod
    def get_last_vacancy_request(self, request: HttpRequest, vacancy_id: int = Query(...)) -> VacancyRequestOut:
        pass


class VacancyRequestsRouter(Router):
    def __init__(self, vacancy_requests_handlers: IVacancyRequestsHandlers, auth: HttpBearer):
        super(VacancyRequestsRouter, self).__init__(tags=[VACANCY_REQUEST_TAG])

        self.add_api_operation(
            path="",
            methods=["POST"],
            view_func=vacancy_requests_handlers.create_vacancy_request,
            auth=[auth],
            response={200: VacancyRequestOut, 401: MessageResponse, 404: MessageResponse, 422: DomainErrorResponse},
            description=f"""
    422 error codes:
        1 - the resume file is not pdf
        2 - size of a resume file must be lte than {settings.MAX_FILE_SIZE_BYTES} bytes"
    """,
        )

        self.add_api_operation(
            path="/last",
            methods=["GET"],
            view_func=vacancy_requests_handlers.get_last_vacancy_request,
            auth=[auth],
            response={200: VacancyRequestOut, 401: MessageResponse, 404: MessageResponse},
        )
