from abc import ABC, abstractmethod

from django.http import HttpRequest
from ninja import Body, File, Path, Router, UploadedFile
from ninja.security import HttpBearer

from api.internal.v1.responses import ErrorResponse, MessageResponse, SuccessResponse
from api.internal.v1.tags import NOT_IMPLEMENTED_TAG
from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    EmailIn,
    NameIn,
    PasswordUpdatedAtOut,
    PhotoOut,
    RegistrationIn,
    ResetPasswordIn,
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
    ) -> PasswordUpdatedAtOut:
        pass


class IUserHandlers(ABC):
    @abstractmethod
    def get_user(self, request: HttpRequest, user_id: int = Path(...)) -> UserOut:
        pass

    @abstractmethod
    def delete_user(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def change_photo(self, request: HttpRequest, user_id: int = Path(...), photo: UploadedFile = File(...)) -> PhotoOut:
        pass

    @abstractmethod
    def remove_photo(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def change_email(
        self, request: HttpRequest, user_id: int = Path(...), body: EmailIn = Body(...)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def rename_user(self, request: HttpRequest, user_id: int = Path(...), body: NameIn = Body(...)) -> SuccessResponse:
        pass


class UsersRouter(Router):
    def __init__(self, user_router: Router, auth_handlers: IAuthHandlers):
        super(UsersRouter, self).__init__(tags=[USERS_TAG])

        self.add_api_operation(
            path="",
            methods=["POST"],
            view_func=auth_handlers.register_user,
            response={200: SuccessResponse, 422: ErrorResponse},
        )

        self.add_api_operation(
            path="/authenticate",
            methods=["POST"],
            view_func=auth_handlers.authenticate_user,
            response={200: AuthenticationOut, 401: MessageResponse},
        )

        self.add_api_operation(
            path="/refresh-tokens",
            methods=["POST"],
            view_func=auth_handlers.refresh_tokens,
            response={200: AuthenticationOut, 400: MessageResponse},
        )

        self.add_router("/{int:user_id}", user_router)


class UserRouter(Router):
    def __init__(self, user_handlers: IUserHandlers, auth_handlers: IAuthHandlers, auth: HttpBearer):
        super(UserRouter, self).__init__(tags=[USERS_TAG])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=user_handlers.get_user,
            response={200: UserOut, 404: MessageResponse},
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["DELETE"],
            view_func=user_handlers.delete_user,
            auth=[auth],
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 422: ErrorResponse},
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_IMPLEMENTED_TAG],
            path="/photo",
            methods=["PATCH"],
            view_func=user_handlers.change_photo,
            auth=[auth],
            response={
                200: PhotoOut,
                401: ErrorResponse,
                404: ErrorResponse,
            },
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_IMPLEMENTED_TAG],
            path="/photo/remove",
            methods=["PATCH"],
            view_func=user_handlers.remove_photo,
            auth=[auth],
            response={
                200: SuccessResponse,
                401: ErrorResponse,
                404: ErrorResponse,
            },
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_IMPLEMENTED_TAG],
            path="/email",
            methods=["PATCH"],
            view_func=user_handlers.change_email,
            auth=[auth],
            response={
                200: SuccessResponse,
                401: ErrorResponse,
                404: ErrorResponse,
                422: ErrorResponse,
            },
        )

        self.add_api_operation(
            tags=[USERS_TAG, NOT_IMPLEMENTED_TAG],
            path="/rename",
            methods=["PATCH"],
            view_func=user_handlers.rename_user,
            auth=[auth],
            response={
                200: SuccessResponse,
                401: ErrorResponse,
                404: ErrorResponse,
            },
        )

        self.add_api_operation(
            path="/reset-password",
            methods=["PATCH"],
            view_func=auth_handlers.reset_password,
            auth=[auth],
            response={
                200: PasswordUpdatedAtOut,
                401: MessageResponse,
                403: MessageResponse,
                422: ErrorResponse,
            },
        )
