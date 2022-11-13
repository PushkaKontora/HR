from abc import ABC, abstractmethod
from typing import Optional

from django.http import HttpRequest
from ninja import File, Form, Query, UploadedFile

from api.internal.v1.errors import NotFoundError
from api.internal.v1.vacancy_requests.domain.entities import RequestIn, RequestOut
from api.internal.v1.vacancy_requests.presentation.errors import ResumeIsLargeError, ResumeIsNotPDFError
from api.internal.v1.vacancy_requests.presentation.routers import IVacancyRequestsHandlers
from api.models import User


class ICreatingRequestService(ABC):
    @abstractmethod
    def exists_vacancy(self, extra: RequestIn) -> bool:
        pass

    @abstractmethod
    def create_request(self, auth_user: User, extra: RequestIn, resume: Optional[UploadedFile]) -> RequestOut:
        pass


class IGettingService(ABC):
    @abstractmethod
    def try_get_last_request_by_owner_and_vacancy_id(self, auth_user: User, vacancy_id: int) -> Optional[RequestOut]:
        pass


class IDocumentService(ABC):
    @abstractmethod
    def is_pdf(self, document: UploadedFile) -> bool:
        pass

    @abstractmethod
    def is_large(self, document: UploadedFile) -> bool:
        pass


class VacancyRequestsHandlers(IVacancyRequestsHandlers):
    def __init__(
        self,
        creating_request_service: ICreatingRequestService,
        getting_service: IGettingService,
        document_service: IDocumentService,
    ):
        self.document_service = document_service
        self.getting_service = getting_service
        self.creating_request_service = creating_request_service

    def create_vacancy_request(
        self, request: HttpRequest, extra: RequestIn = Form(...), resume: Optional[UploadedFile] = File(None)
    ) -> RequestOut:
        if not self.creating_request_service.exists_vacancy(extra):
            raise NotFoundError()

        if resume is not None:
            if not self.document_service.is_pdf(resume):
                raise ResumeIsNotPDFError()

            if self.document_service.is_large(resume):
                raise ResumeIsLargeError()

        return self.creating_request_service.create_request(request.user, extra, resume)

    def get_last_vacancy_request(self, request: HttpRequest, vacancy_id: int = Query(...)) -> RequestOut:
        request_out = self.getting_service.try_get_last_request_by_owner_and_vacancy_id(request.user, vacancy_id)

        if not request_out:
            raise NotFoundError()

        return request_out
