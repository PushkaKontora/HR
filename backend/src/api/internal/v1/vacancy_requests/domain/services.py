from abc import ABC, abstractmethod
from typing import Optional

from django.conf import settings
from django.db.transaction import atomic
from ninja import UploadedFile

from api.internal.v1.vacancy_requests.domain.entities import RequestIn, VacancyRequestOut
from api.internal.v1.vacancy_requests.domain.notifiers import IVacancyRequestNotifier
from api.internal.v1.vacancy_requests.presentation.handlers import (
    ICreatingRequestService,
    IDocumentService,
    IGettingService,
)
from api.models import User, VacancyRequest


class IUserRepository(ABC):
    @abstractmethod
    def get_employer_by_vacancy_id(self, vacancy_id: int) -> User:
        pass


class IVacancyRequestRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, vacancy_id: int) -> VacancyRequest:
        pass

    @abstractmethod
    def try_get_last_by_owner_id_and_vacancy_id(self, owner_id: int, vacancy_id: int) -> Optional[VacancyRequest]:
        pass


class IVacancyRepository(ABC):
    @abstractmethod
    def exists_vacancy_with_id(self, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def exists_published_vacancy_with_id(self, vacancy_id: int) -> bool:
        pass


class CreatingRequestService(ICreatingRequestService):
    def __init__(
        self,
        user_repo: IUserRepository,
        vacancy_repo: IVacancyRepository,
        vacancy_request_repo: IVacancyRequestRepository,
        employer_notifier: IVacancyRequestNotifier,
    ):
        self.vacancy_repo = vacancy_repo
        self.employer_notifier = employer_notifier
        self.vacancy_request_repo = vacancy_request_repo
        self.user_repo = user_repo

    def exists_vacancy(self, extra: RequestIn) -> bool:
        return self.vacancy_repo.exists_vacancy_with_id(extra.vacancy_id)

    def exists_published_vacancy(self, extra: RequestIn) -> bool:
        return self.vacancy_repo.exists_published_vacancy_with_id(extra.vacancy_id)

    @atomic
    def create_request(self, auth_user: User, extra: RequestIn, resume: Optional[UploadedFile]) -> VacancyRequestOut:
        employer = self.user_repo.get_employer_by_vacancy_id(extra.vacancy_id)

        request = self.vacancy_request_repo.create(auth_user.id, extra.vacancy_id)
        self.employer_notifier.notify(request, auth_user, employer, extra, resume)

        return VacancyRequestOut.from_request(request)


class DocumentService(IDocumentService):
    def is_pdf(self, document: UploadedFile) -> bool:
        return document.content_type == "application/pdf"

    def is_large(self, document: UploadedFile) -> bool:
        return document.size > settings.MAX_FILE_SIZE_BYTES


class GettingService(IGettingService):
    def __init__(self, vacancy_request_repo: IVacancyRequestRepository):
        self.vacancy_request_repo = vacancy_request_repo

    def try_get_last_request_by_owner_and_vacancy_id(
        self, auth_user: User, vacancy_id: int
    ) -> Optional[VacancyRequestOut]:
        request = self.vacancy_request_repo.try_get_last_by_owner_id_and_vacancy_id(auth_user.id, vacancy_id)

        if not request:
            return None

        return VacancyRequestOut.from_request(request)
