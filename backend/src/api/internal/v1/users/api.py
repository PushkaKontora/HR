from typing import Type

from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.v1.errors import DomainErrorBase
from api.internal.v1.users.db.repositories import (
    DepartmentRepository,
    IssuedTokenRepository,
    PasswordRepository,
    UserRepository,
)
from api.internal.v1.users.domain.services import (
    AuthenticationService,
    ChangingEmailService,
    DeletingUserService,
    GettingUserService,
    JWTService,
    PhotoService,
    RegistrationService,
    RenamingUserService,
    ResettingPasswordService,
)
from api.internal.v1.users.presentation.authentication import JWTAuth
from api.internal.v1.users.presentation.errors import (
    EmailHasAlreadyRegisteredError,
    EmailIsAlreadyRegisteredError,
    FileIsNotImageError,
    PasswordDoesNotMatchError,
    UserIsLeaderOfDepartmentError,
)
from api.internal.v1.users.presentation.handlers import AuthHandlers, UserHandlers
from api.internal.v1.users.presentation.routers import UserRouter, UsersRouter

ERRORS = [
    EmailHasAlreadyRegisteredError,
    PasswordDoesNotMatchError,
    UserIsLeaderOfDepartmentError,
    EmailIsAlreadyRegisteredError,
    FileIsNotImageError,
]


class UsersContainer(containers.DeclarativeContainer):
    user_repo = providers.Singleton(UserRepository)
    password_repo = providers.Singleton(PasswordRepository)
    issued_token_repo = providers.Singleton(IssuedTokenRepository)
    department_repo = providers.Singleton(DepartmentRepository)

    registration_service = providers.Singleton(RegistrationService, user_repo=user_repo, password_repo=password_repo)
    auth_service = providers.Singleton(AuthenticationService, user_repo=user_repo)
    jwt_service = providers.Singleton(JWTService, issued_token_repo=issued_token_repo, user_repo=user_repo)
    getting_user_service = providers.Singleton(GettingUserService, user_repo=user_repo)
    resetting_password_service = providers.Singleton(ResettingPasswordService)
    deleting_user_service = providers.Singleton(
        DeletingUserService, user_repo=user_repo, department_repo=department_repo
    )
    renaming_user_service = providers.Singleton(RenamingUserService, user_repo=user_repo)
    changing_email_service = providers.Singleton(ChangingEmailService, user_repo=user_repo)
    photo_service = providers.Singleton(PhotoService, user_repo=user_repo)

    auth = providers.Singleton(JWTAuth, jwt_service=jwt_service)
    auth_handlers = providers.Singleton(
        AuthHandlers,
        registration_service=registration_service,
        auth_service=auth_service,
        jwt_service=jwt_service,
        resetting_password_service=resetting_password_service,
        getting_user_service=getting_user_service,
    )
    user_handlers = providers.Singleton(
        UserHandlers,
        getting_user_service=getting_user_service,
        deleting_user_service=deleting_user_service,
        renaming_user_service=renaming_user_service,
        changing_email_service=changing_email_service,
        photo_service=photo_service,
    )

    user_router = providers.Singleton(UserRouter, user_handlers=user_handlers, auth_handlers=auth_handlers, auth=auth)
    users_router = providers.Singleton(UsersRouter, user_router=user_router, auth_handlers=auth_handlers)


def register_users_api(base: NinjaAPI) -> None:
    container = UsersContainer()

    for exception_cls in ERRORS:
        base.add_exception_handler(exception_cls, _get_handler(exception_cls))

    base.add_router("/users", container.users_router())


def _get_handler(exception_cls: Type[DomainErrorBase]):
    return lambda request, exc: exception_cls.response(exc)
