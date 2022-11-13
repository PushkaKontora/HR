from typing import Type

from dependency_injector import containers, providers
from ninja import NinjaAPI
from ninja.security import HttpBearer

from api.internal.v1.errors import DomainErrorBase
from api.internal.v1.users.api import UsersContainer
from api.internal.v1.vacancy_requests.db.repositories import UserRepository, VacancyRepository, VacancyRequestRepository
from api.internal.v1.vacancy_requests.domain.notifiers import EmailNotifier
from api.internal.v1.vacancy_requests.domain.services import CreatingRequestService, DocumentService, GettingService
from api.internal.v1.vacancy_requests.presentation.errors import ResumeIsLargeError, ResumeIsNotPDFError
from api.internal.v1.vacancy_requests.presentation.handlers import VacancyRequestsHandlers
from api.internal.v1.vacancy_requests.presentation.routers import VacancyRequestsRouter

ERRORS = [ResumeIsNotPDFError, ResumeIsLargeError]


class VacancyRequestsContainer(containers.DeclarativeContainer):
    auth = providers.ExternalDependency(HttpBearer)
    employer_notifier = providers.Factory(EmailNotifier)

    user_repo = providers.Singleton(UserRepository)
    vacancy_repo = providers.Singleton(VacancyRepository)
    vacancy_request_repo = providers.Singleton(VacancyRequestRepository)

    creating_request_service = providers.Singleton(
        CreatingRequestService,
        user_repo=user_repo,
        vacancy_request_repo=vacancy_request_repo,
        vacancy_repo=vacancy_repo,
        employer_notifier=employer_notifier,
    )
    getting_service = providers.Singleton(GettingService, vacancy_request_repo=vacancy_request_repo)

    vacancy_requests_handlers = providers.Singleton(
        VacancyRequestsHandlers,
        creating_request_service=creating_request_service,
        getting_service=getting_service,
        document_service=providers.Singleton(DocumentService),
    )

    vacancy_requests_router = providers.Singleton(
        VacancyRequestsRouter, vacancy_requests_handlers=vacancy_requests_handlers, auth=auth
    )


def register_vacancy_requests_api(base: NinjaAPI) -> None:
    container = VacancyRequestsContainer(auth=UsersContainer().auth())

    for error in ERRORS:
        base.add_exception_handler(error, _get_handler(error))

    base.add_router("/vacancy-requests", container.vacancy_requests_router())


def _get_handler(error: Type[DomainErrorBase]):
    return lambda request, exc: error.response(exc)
