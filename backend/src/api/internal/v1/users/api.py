from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.v1.users.presentation.handlers import AuthHandlers, UserHandlers
from api.internal.v1.users.presentation.routers import get_users_router


class Container(containers.DeclarativeContainer):
    auth_handlers = providers.Singleton(AuthHandlers)
    user_handlers = providers.Singleton(UserHandlers)


def register_users_api(base: NinjaAPI) -> None:
    container = Container()

    router = get_users_router(container.auth_handlers(), container.user_handlers())

    base.add_router("/users", router)
