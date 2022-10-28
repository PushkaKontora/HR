from typing import Type

from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.v1.authentication import JWTBaseAuthentication
from api.internal.v1.exceptions import APIBaseException
from api.internal.v1.users.db.repositories import IssuedTokenRepository, PasswordRepository, UserRepository
from api.internal.v1.users.domain.services import AuthenticationService, JWTService, RegistrationService
from api.internal.v1.users.presentation.exceptions import PasswordHasAlreadyRegistered
from api.internal.v1.users.presentation.handlers import AuthHandlers, UserHandlers
from api.internal.v1.users.presentation.routers import UserRouter, UsersRouter
from api.models import User

EXCEPTIONS = [PasswordHasAlreadyRegistered]


class AnyUserStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class Container(containers.DeclarativeContainer):
    any_user = providers.Factory(AnyUserStub)

    user_repo = providers.Singleton(UserRepository)
    password_repo = providers.Singleton(PasswordRepository)
    issued_token_repo = providers.Singleton(IssuedTokenRepository)

    registration_service = providers.Singleton(RegistrationService, user_repo=user_repo, password_repo=password_repo)
    auth_service = providers.Singleton(AuthenticationService, user_repo=user_repo)
    jwt_service = providers.Singleton(JWTService, issued_token_repo=issued_token_repo)

    auth_handlers = providers.Singleton(
        AuthHandlers, registration_service=registration_service, auth_service=auth_service, jwt_service=jwt_service
    )
    user_handlers = providers.Singleton(UserHandlers)

    user_router = providers.Singleton(
        UserRouter, user_handlers=user_handlers, auth_handlers=auth_handlers, any_user=any_user
    )
    users_router = providers.Singleton(UsersRouter, user_router=user_router, auth_handlers=auth_handlers)


def register_users_api(base: NinjaAPI) -> None:
    container = Container()

    for exception_cls in EXCEPTIONS:
        base.add_exception_handler(exception_cls, _get_handler(exception_cls))

    base.add_router("/users", container.users_router())


def _get_handler(exception_cls: Type[APIBaseException]):
    return lambda request, exc: exception_cls.response(exc)
