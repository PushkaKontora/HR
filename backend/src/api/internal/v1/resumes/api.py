from dependency_injector import containers, providers
from ninja import NinjaAPI
from ninja.security import HttpBearer

from api.internal.v1.resumes.presentation.handlers import ResumeHandlers, ResumesHandlers, ResumesWishlistHandlers
from api.internal.v1.resumes.presentation.routers import ResumeRouter, ResumesRouter, ResumesWishlistRouter
from api.internal.v1.users.api import UsersContainer


class ResumesContainer(containers.DeclarativeContainer):
    auth = providers.ExternalDependency(HttpBearer)

    resume_handlers = providers.Singleton(ResumeHandlers)
    resumes_handlers = providers.Singleton(ResumesHandlers)
    wishlist_resumes_handlers = providers.Singleton(ResumesWishlistHandlers)

    resume_router = providers.Singleton(
        ResumeRouter,
        resume_handlers=resume_handlers,
        auth=auth,
    )
    resumes_wishlist_router = providers.Singleton(
        ResumesWishlistRouter, wishlist_resumes_handlers=wishlist_resumes_handlers, auth=auth
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

    base.add_router("/resumes", container.resumes_router())
