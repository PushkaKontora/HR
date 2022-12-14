from abc import ABC, abstractmethod

from django.http import HttpRequest
from ninja import Body, File, Path, Router, UploadedFile
from ninja.security import HttpBearer

from api.internal.responses import DomainErrorResponse, MessageResponse, SuccessResponse
from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    EmailIn,
    NameIn,
    PhotoOut,
    RegistrationIn,
    ResettingPasswordIn,
    UpdatingPasswordOut,
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
        self, request: HttpRequest, user_id: int = Path(...), body: ResettingPasswordIn = Body(...)
    ) -> UpdatingPasswordOut:
        pass


class IUserHandlers(ABC):
    @abstractmethod
    def get_user(self, request: HttpRequest, user_id: int = Path(...)) -> UserOut:
        pass

    @abstractmethod
    def delete_user(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def upload_photo(self, request: HttpRequest, user_id: int = Path(...), photo: UploadedFile = File(...)) -> PhotoOut:
        pass

    @abstractmethod
    def delete_photo(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
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
            response={200: SuccessResponse, 422: DomainErrorResponse},
            description="""
    422 error codes:
        1 - the email has already registered
    """,
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
            auth=[auth],
            response={200: UserOut, 403: MessageResponse, 404: MessageResponse},
        )

        self.add_api_operation(
            path="",
            methods=["DELETE"],
            view_func=user_handlers.delete_user,
            auth=[auth],
            response={
                200: SuccessResponse,
                401: MessageResponse,
                403: MessageResponse,
                404: MessageResponse,
                422: DomainErrorResponse,
            },
            description="""
    422 error codes:
        10 - the user is a leader of a department
    """,
        )

        self.add_api_operation(
            path="/photo",
            methods=["POST"],
            view_func=user_handlers.upload_photo,
            auth=[auth],
            response={200: PhotoOut, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
            description="""
    422 error codes:
        12 - the file is not an image
    """,
        )

        self.add_api_operation(
            path="/photo",
            methods=["DELETE"],
            view_func=user_handlers.delete_photo,
            auth=[auth],
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
        )

        self.add_api_operation(
            path="/email",
            methods=["PATCH"],
            view_func=user_handlers.change_email,
            auth=[auth],
            response={
                200: SuccessResponse,
                401: MessageResponse,
                403: MessageResponse,
                404: MessageResponse,
                422: DomainErrorResponse,
            },
            description="""
    422 error codes:
        11 - the email is already registered
    """,
        )

        self.add_api_operation(
            path="/rename",
            methods=["PATCH"],
            view_func=user_handlers.rename_user,
            auth=[auth],
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
        )

        self.add_api_operation(
            path="/reset-password",
            methods=["PATCH"],
            view_func=auth_handlers.reset_password,
            auth=[auth],
            response={
                200: UpdatingPasswordOut,
                401: MessageResponse,
                403: MessageResponse,
                404: MessageResponse,
                422: DomainErrorResponse,
            },
            description="""
    422 error codes:
        2 - the previous password does not match with expected
    """,
        )
