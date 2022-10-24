from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.authentication import JWTBaseAuthentication
from api.internal.models import User
from api.internal.v1.users.presentation.handlers import AuthHandlers, UserHandlers
from api.internal.v1.users.presentation.routers import UserRouter, UsersRouter


class AnyUserStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass


class Container(containers.DeclarativeContainer):
    any_user = providers.Factory(AnyUserStub)

    auth_handlers = providers.Singleton(AuthHandlers)
    user_handlers = providers.Singleton(UserHandlers)

    user_router = providers.Singleton(
        UserRouter, user_handlers=user_handlers, auth_handlers=auth_handlers, any_user=any_user
    )
    users_router = providers.Singleton(UsersRouter, user_router=user_router, auth_handlers=auth_handlers)


def register_users_api(base: NinjaAPI) -> None:
    container = Container()

    base.add_router("/users", container.users_router())
