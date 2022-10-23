from abc import ABC, abstractmethod

from django.http import HttpRequest
from ninja import Body, File, Path, Router, UploadedFile

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
        self, request: HttpRequest, user_id: int = Path(..., alias="userId"), body: ResetPasswordIn = Body(...)
    ) -> ResetPasswordOut:
        pass


class IUserHandlers(ABC):
    @abstractmethod
    def get_user(self, request: HttpRequest, user_id: int = Path(..., alias="userId")) -> UserOut:
        pass

    @abstractmethod
    def delete_user(self, request: HttpRequest, user_id: int = Path(..., alias="userId")) -> SuccessResponse:
        pass

    @abstractmethod
    def change_photo(
        self, request: HttpRequest, user_id: int = Path(..., alias="userId"), photo: UploadedFile = File(...)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def change_email(
        self, request: HttpRequest, user_id: int = Path(..., alias="userId"), body: EmailIn = Body(...)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def rename(self, request: HttpRequest, user_id: int = Path(..., alias="userId"), body: NameIn = Body(...)) -> SuccessResponse:
        pass


def get_users_router(auth_handlers: IAuthHandlers, user_handlers: IUserHandlers) -> Router:
    router = Router(tags=[USERS_TAG])

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="",
        methods=["POST"],
        view_func=auth_handlers.register_user,
        response={200: SuccessResponse, 422: ErrorResponse},
    )

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="/authenticate",
        methods=["POST"],
        view_func=auth_handlers.authenticate_user,
        response={200: AuthenticationOut, 401: ErrorResponse},
    )

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="/refresh-tokens",
        methods=["POST"],
        view_func=auth_handlers.refresh_tokens,
        response={200: AuthenticationOut, 401: ErrorResponse, 422: ErrorResponse},
    )

    router.add_router("/{int:userId}", get_user_router(user_handlers, auth_handlers))

    return router


def get_user_router(user_handlers: IUserHandlers, auth_handlers: IAuthHandlers) -> Router:
    router = Router(tags=[USERS_TAG])

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="",
        methods=["GET"],
        view_func=user_handlers.get_user,
        response={200: UserOut, 404: ErrorResponse},
    )

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="",
        methods=["DELETE"],
        view_func=user_handlers.delete_user,
        response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse},
    )

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="/photo",
        methods=["PATCH"],
        view_func=user_handlers.change_photo,
        response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse, 422: ErrorResponse},
    )

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="/email",
        methods=["PATCH"],
        view_func=user_handlers.change_email,
        response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse, 422: ErrorResponse},
    )

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="/rename",
        methods=["PATCH"],
        view_func=user_handlers.rename,
        response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse, 422: ErrorResponse},
    )

    router.add_api_operation(
        tags=[USERS_TAG, NOT_READY_TAG],
        path="/reset-password",
        methods=["PATCH"],
        view_func=auth_handlers.reset_password,
        response={
            200: ResetPasswordOut,
            401: ErrorResponse,
            403: ErrorResponse,
            404: ErrorResponse,
            422: ErrorResponse,
        },
    )

    return router
