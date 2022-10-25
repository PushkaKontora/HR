from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.authentication import JWTBaseAuthentication
from api.internal.v1.resumes.presentation.handlers import ResumeHandlers, ResumesHandlers, ResumesWishlistHandlers
from api.internal.v1.resumes.presentation.routers import ResumeRouter, ResumesRouter, ResumesWishlistRouter
from api.models import User


class OnlyEmployerStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class AnyUserStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class Container(containers.DeclarativeContainer):
    only_employer = providers.Factory(OnlyEmployerStub)
    any_user = providers.Factory(AnyUserStub)

    resume_handlers = providers.Singleton(ResumeHandlers)
    resumes_handlers = providers.Singleton(ResumesHandlers)
    wishlist_resumes_handlers = providers.Singleton(ResumesWishlistHandlers)

    resume_router = providers.Singleton(
        ResumeRouter,
        resume_handlers=resume_handlers,
        any_user=any_user,
    )
    resumes_wishlist_router = providers.Singleton(
        ResumesWishlistRouter, wishlist_resumes_handlers=wishlist_resumes_handlers, only_employer=only_employer
    )
    resumes_router = providers.Singleton(
        ResumesRouter,
        resume_router=resume_router,
        resumes_wishlist_router=resumes_wishlist_router,
        resumes_handlers=resumes_handlers,
        resume_handlers=resume_handlers,
        any_user=any_user,
    )


def register_resumes_api(base: NinjaAPI) -> None:
    container = Container()

    base.add_router("/resumes", container.resumes_router())
