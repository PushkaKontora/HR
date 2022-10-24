from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.authentication import JWTBaseAuthentication
from api.internal.models import User
from api.internal.v1.resumes.presentation.handlers import ResumeHandlers, ResumesHandlers, ResumesWishlistHandlers
from api.internal.v1.resumes.presentation.routers import ResumeRouter, ResumesRouter, ResumesWishlistRouter


class OnlyOwnerStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class OnlyEmployerStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class OnlySelfStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class Container(containers.DeclarativeContainer):
    only_owner = providers.Factory(OnlyOwnerStub)
    only_employer = providers.Factory(OnlyEmployerStub)
    only_self = providers.Factory(OnlySelfStub)

    resume_handlers = providers.Singleton(ResumeHandlers)
    resumes_handlers = providers.Singleton(ResumesHandlers)
    wishlist_resumes_handlers = providers.Singleton(ResumesWishlistHandlers)

    resume_router = providers.Singleton(
        ResumeRouter,
        resume_handlers=resume_handlers,
        only_owner=only_owner,
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
        only_self=only_self,
    )


def register_resumes_api(base: NinjaAPI) -> None:
    container = Container()

    base.add_router("/resumes", container.resumes_router())
