from django.http import HttpRequest
from ninja import Body, File, Path, UploadedFile

from api.internal.base import SuccessResponse
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
from api.internal.v1.users.presentation.routers import IAuthHandlers, IUserHandlers


class AuthHandlers(IAuthHandlers):
    def register_user(self, request: HttpRequest, body: RegistrationIn = Body(...)) -> SuccessResponse:
        pass

    def authenticate_user(self, request: HttpRequest, body: AuthenticationIn = Body(...)) -> AuthenticationOut:
        pass

    def refresh_tokens(self, request: HttpRequest) -> AuthenticationOut:
        pass

    def reset_password(
        self, request: HttpRequest, user_id: int = Path(...), body: ResetPasswordIn = Body(...)
    ) -> ResetPasswordOut:
        pass


class UserHandlers(IUserHandlers):
    def get_user(self, request: HttpRequest, user_id: int = Path(...)) -> UserOut:
        pass

    def delete_user(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        pass

    def change_photo(
        self, request: HttpRequest, user_id: int = Path(...), photo: UploadedFile = File(...)
    ) -> SuccessResponse:
        pass

    def change_email(
        self, request: HttpRequest, user_id: int = Path(...), body: EmailIn = Body(...)
    ) -> SuccessResponse:
        pass

    def rename(self, request: HttpRequest, user_id: int = Path(...), body: NameIn = Body(...)) -> SuccessResponse:
        pass
