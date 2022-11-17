from abc import ABC, abstractmethod
from typing import Optional

from django.http import HttpRequest
from ninja import File, Form, Query, UploadedFile

from api.internal.errors import NotFoundError
from api.internal.v1.vacancy_requests.domain.entities import RequestIn, VacancyRequestOut
from api.internal.v1.vacancy_requests.presentation.errors import ResumeIsLargeError, ResumeIsNotPDFError
from api.internal.v1.vacancy_requests.presentation.routers import IVacancyRequestsHandlers
from api.logging import get_logger
from api.models import User


class ICreatingRequestService(ABC):
    @abstractmethod
    def exists_vacancy(self, extra: RequestIn) -> bool:
        pass

    @abstractmethod
    def create_request(self, auth_user: User, extra: RequestIn, resume: Optional[UploadedFile]) -> VacancyRequestOut:
        pass

    @abstractmethod
    def exists_published_vacancy(self, extra: RequestIn) -> bool:
        pass


class IGettingService(ABC):
    @abstractmethod
    def try_get_last_request_by_owner_and_vacancy_id(
        self, auth_user: User, vacancy_id: int
    ) -> Optional[VacancyRequestOut]:
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
    ) -> VacancyRequestOut:
        auth_user: User = request.user
        logger = get_logger(request)

        logger.info(
            "Creating a vacancy request auth_user={auth_user} extra={extra} resume={resume}",
            auth_user={"id": auth_user.id},
            extra=extra.dict(),
            resume={"name": resume.name, "content_type": resume.content_type, "size": resume.size}
            if resume is not None
            else None,
        )

        logger.info("Checking an existence of the published vacancy...")
        if not self.creating_request_service.exists_published_vacancy(extra):
            logger.success("Not found the published vacancy")
            raise NotFoundError()

        if resume is not None:
            logger.info("Checking the resume file...")

            if not self.document_service.is_pdf(resume):
                logger.success("The resume file is not pdf")
                raise ResumeIsNotPDFError()

            if self.document_service.is_large(resume):
                logger.success("Size of the resume file is large")
                raise ResumeIsLargeError()

        logger.info("Creating a vacancy request...")
        vacancy_request_out = self.creating_request_service.create_request(auth_user, extra, resume)
        logger.success("The vacancy request was created")

        return vacancy_request_out

    def get_last_vacancy_request(self, request: HttpRequest, vacancy_id: int = Query(...)) -> VacancyRequestOut:
        request_out = self.getting_service.try_get_last_request_by_owner_and_vacancy_id(request.user, vacancy_id)

        if not request_out:
            raise NotFoundError()

        return request_out
