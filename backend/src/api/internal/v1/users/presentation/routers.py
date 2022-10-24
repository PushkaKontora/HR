from abc import ABC, abstractmethod

from django.http import HttpRequest
from ninja import Body, File, Path, Router, UploadedFile

from api.internal.authentication import JWTBaseAuthentication
from api.internal.base import NOT_READY_TAG, ErrorResponse, SuccessResponse
from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    EmailIn,
    NameIn,
    RegistrationIn,
    ResetPasswordIn,
    ResetPasswordOut,
    UserOut,
)

USERS_TAG = "users"


class IAuthHandlers(ABC):
    @abstractmethod
    def register_user(self, request: HttpRequest, body: RegistrationIn = Body(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def authenticate_user(self, request: HttpRequest, body: AuthenticationIn = Body(...)) -> AuthenticationOut:
        pass

    @abstractmethod
    def refresh_tokens(self, request: HttpRequest) -> AuthenticationOut:
        pass

    @abstractmethod
    def reset_password(
        self, request: HttpRequest, user_id: int = Path(...), body: ResetPasswordIn = Body(...)
    ) -> ResetPasswordOut:
        pass


class IUserHandlers(ABC):
    @abstractmethod
    def get_user(self, request: HttpRequest, user_id: int = Path(...)) -> UserOut:
        pass

    @abstractmethod
    def delete_user(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def change_photo(
        self, request: HttpRequest, user_id: int = Path(...), photo: UploadedFile = File(...)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def change_email(
        self, request: HttpRequest, user_id: int = Path(...), body: EmailIn = Body(...)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def rename(self, request: HttpRequest, user_id: int = Path(...), body: NameIn = Body(...)) -> SuccessResponse:
        pass


class UsersRouter(Router):
    def __init__(self, user_router: Router, auth_handlers: IAuthHandlers):
        super(UsersRouter, self).__init__(tags=[USERS_TAG])

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="",
            methods=["POST"],
            view_func=auth_handlers.register_user,
            response={200: SuccessResponse, 422: ErrorResponse},
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="/authenticate",
            methods=["POST"],
            view_func=auth_handlers.authenticate_user,
            response={200: AuthenticationOut, 401: ErrorResponse},
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="/refresh-tokens",
            methods=["POST"],
            view_func=auth_handlers.refresh_tokens,
            response={200: AuthenticationOut, 401: ErrorResponse, 422: ErrorResponse},
        )

        self.add_router("/{int:user_id}", user_router)


class UserRouter(Router):
    def __init__(self, user_handlers: IUserHandlers, auth_handlers: IAuthHandlers, only_self: JWTBaseAuthentication):
        super(UserRouter, self).__init__(tags=[USERS_TAG])

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="",
            methods=["GET"],
            view_func=user_handlers.get_user,
            response={200: UserOut, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="",
            methods=["DELETE"],
            view_func=user_handlers.delete_user,
            auth=[only_self],
            response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="/photo",
            methods=["PATCH"],
            view_func=user_handlers.change_photo,
            auth=[only_self],
            response={
                200: SuccessResponse,
                401: ErrorResponse,
                403: ErrorResponse,
                404: ErrorResponse,
                422: ErrorResponse,
            },
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="/email",
            methods=["PATCH"],
            view_func=user_handlers.change_email,
            auth=[only_self],
            response={
                200: SuccessResponse,
                401: ErrorResponse,
                403: ErrorResponse,
                404: ErrorResponse,
                422: ErrorResponse,
            },
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="/rename",
            methods=["PATCH"],
            view_func=user_handlers.rename,
            auth=[only_self],
            response={
                200: SuccessResponse,
                401: ErrorResponse,
                403: ErrorResponse,
                404: ErrorResponse,
                422: ErrorResponse,
            },
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_READY_TAG],
            path="/reset-password",
            methods=["PATCH"],
            view_func=auth_handlers.reset_password,
            auth=[only_self],
            response={
                200: ResetPasswordOut,
                401: ErrorResponse,
                403: ErrorResponse,
                404: ErrorResponse,
                422: ErrorResponse,
            },
        )
