from typing import Type

from dependency_injector import containers, providers
from ninja import NinjaAPI
from ninja.security import HttpBearer

from api.internal.v1.exceptions import APIBaseError
from api.internal.v1.resumes.db.repositories import (
    CompetencyRepository,
    FavouriteResumeRepository,
    ResumeCompetenciesRepository,
    ResumeRepository,
)
from api.internal.v1.resumes.db.searchers import (
    CompetenciesSearcher,
    DesiredJobSearcher,
    ExperienceSearcher,
    PublishedStatusSearcher,
    SalaryFromSearcher,
    SalaryToSearcher,
)
from api.internal.v1.resumes.db.sorters import SortByAddedAtDESC, SortByPublishedAtASC
from api.internal.v1.resumes.domain.services import (
    CreatingResumeService,
    DocumentService,
    GettingResumeService,
    GettingResumesService,
    PublishingResumeService,
    ResumesWishlistService,
    UpdatingResumeService,
)
from api.internal.v1.resumes.presentation.exceptions import (
    AttachedDocumentIsNotPDFError,
    ResumeAlreadyAddedToWishlistError,
    ResumeIsCreatedByUserError,
)
from api.internal.v1.resumes.presentation.handlers import ResumeHandlers, ResumesHandlers, ResumesWishlistHandlers
from api.internal.v1.resumes.presentation.routers import ResumeRouter, ResumesRouter, ResumesWishlistRouter
from api.internal.v1.users.api import UsersContainer

ERRORS = [ResumeIsCreatedByUserError, AttachedDocumentIsNotPDFError, ResumeAlreadyAddedToWishlistError]


class ResumesContainer(containers.DeclarativeContainer):
    auth = providers.ExternalDependency(HttpBearer)

    resumes_published_at_asc_sorter = providers.Factory(SortByPublishedAtASC)
    resumes_added_at_desc_sorter = providers.Factory(SortByAddedAtDESC)
    desired_job_searcher = providers.Factory(DesiredJobSearcher)
    experience_searcher = providers.Factory(ExperienceSearcher)
    salary_from_searcher = providers.Factory(SalaryFromSearcher)
    salary_to_searcher = providers.Factory(SalaryToSearcher)
    competencies_searcher = providers.Factory(CompetenciesSearcher)
    published_status_searcher = providers.Factory(PublishedStatusSearcher)

    resume_repo = providers.Singleton(
        ResumeRepository,
        desired_job_searcher=desired_job_searcher,
        experience_searcher=experience_searcher,
        salary_from_searcher=salary_from_searcher,
        salary_to_searcher=salary_to_searcher,
        competencies_searcher=competencies_searcher,
        published_status_searcher=published_status_searcher,
    )
    competency_repo = providers.Singleton(CompetencyRepository)
    resume_competencies_repo = providers.Singleton(ResumeCompetenciesRepository)
    favourite_resume_repo = providers.Singleton(
        FavouriteResumeRepository,
        resumes_published_at_asc_sorter=resumes_published_at_asc_sorter,
        resumes_added_at_desc_sorter=resumes_added_at_desc_sorter,
    )

    creating_resume_service = providers.Singleton(
        CreatingResumeService,
        resume_repo=resume_repo,
        competency_repo=competency_repo,
        resume_competencies_repo=resume_competencies_repo,
    )
    publishing_resume_service = providers.Singleton(PublishingResumeService, resume_repo=resume_repo)
    getting_resume_service = providers.Singleton(GettingResumeService, resume_repo=resume_repo)
    getting_resumes_service = providers.Singleton(GettingResumesService, resume_repo=resume_repo)
    document_service = providers.Singleton(DocumentService)
    updating_resume_service = providers.Singleton(
        UpdatingResumeService,
        resume_repo=resume_repo,
        competency_repo=competency_repo,
        resume_competencies_repo=resume_competencies_repo,
    )
    resumes_wishlist_service = providers.Singleton(
        ResumesWishlistService,
        favourite_resume_repo=favourite_resume_repo,
    )

    resume_handlers = providers.Singleton(
        ResumeHandlers,
        creating_resume_service=creating_resume_service,
        publishing_resume_service=publishing_resume_service,
        getting_resume_service=getting_resume_service,
        document_service=document_service,
        updating_resume_service=updating_resume_service,
    )
    resumes_handlers = providers.Singleton(ResumesHandlers, getting_resumes_service)
    resumes_wishlist_handlers = providers.Singleton(
        ResumesWishlistHandlers,
        resumes_wishlist_service=resumes_wishlist_service,
        getting_resume_service=getting_resume_service,
    )

    resume_router = providers.Singleton(
        ResumeRouter,
        resume_handlers=resume_handlers,
        auth=auth,
    )
    resumes_wishlist_router = providers.Singleton(
        ResumesWishlistRouter, resumes_wishlist_handlers=resumes_wishlist_handlers, auth=auth
    )
    resumes_router = providers.Singleton(
        ResumesRouter,
        resume_router=resume_router,
        resumes_wishlist_router=resumes_wishlist_router,
        resumes_handlers=resumes_handlers,
        resume_handlers=resume_handlers,
        auth=auth,
    )


def register_resumes_api(base: NinjaAPI) -> None:
    container = ResumesContainer(auth=UsersContainer().auth())

    for error in ERRORS:
        base.add_exception_handler(error, _get_handler(error))

    base.add_router("/resumes", container.resumes_router())


def _get_handler(error: Type[APIBaseError]):
    return lambda request, exc: error.response(exc)
