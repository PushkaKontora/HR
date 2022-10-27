from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.http import HttpRequest
from ninja import Body, File, Path, UploadedFile
from ninja.responses import Response

from api.internal.v1.exceptions import Unauthorized
from api.internal.v1.responses import SuccessResponse
from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    EmailIn,
    NameIn,
    RegistrationIn,
    ResetPasswordIn,
    ResetPasswordOut,
    Tokens,
    UserOut,
)
from api.internal.v1.users.presentation.exceptions import PasswordHasAlreadyRegistered
from api.internal.v1.users.presentation.routers import IAuthHandlers, IUserHandlers


class IRegistrationService(ABC):
    @abstractmethod
    def is_email_taken(self, email: str) -> bool:
        pass

    @abstractmethod
    def register(self, body: RegistrationIn) -> None:
        pass


class IAuthenticationService(ABC):
    @abstractmethod
    def authenticate(self, body: AuthenticationIn) -> Optional[Tokens]:
        pass

    @abstractmethod
    def get_authentication_out(self, tokens: Tokens) -> AuthenticationOut:
        pass


class AuthHandlers(IAuthHandlers):
    def __init__(self, registration_service: IRegistrationService, auth_service: IAuthenticationService):
        self.auth_service = auth_service
        self.registration_service = registration_service

    def register_user(self, request: HttpRequest, body: RegistrationIn = Body(...)) -> SuccessResponse:
        if self.registration_service.is_email_taken(body.email):
            raise PasswordHasAlreadyRegistered()

        self.registration_service.register(body)

        return SuccessResponse()

    def authenticate_user(self, request: HttpRequest, body: AuthenticationIn = Body(...)) -> Response:
        tokens = self.auth_service.authenticate(body)

        if not tokens:
            raise Unauthorized()

        response = Response(self.auth_service.get_authentication_out(tokens))
        response.set_cookie(
            key=settings.REFRESH_TOKEN_COOKIE,
            value=tokens.refresh,
            httponly=True,
            expires=datetime.utcnow() + settings.REFRESH_TOKEN_TTL,
        )

        return response

    def refresh_tokens(self, request: HttpRequest) -> AuthenticationOut:
        raise NotImplementedError()

    def reset_password(
        self, request: HttpRequest, user_id: int = Path(...), body: ResetPasswordIn = Body(...)
    ) -> ResetPasswordOut:
        raise NotImplementedError()


class UserHandlers(IUserHandlers):
    def remove_photo(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        raise NotImplementedError()

    def get_user(self, request: HttpRequest, user_id: int = Path(...)) -> UserOut:
        raise NotImplementedError()

    def delete_user(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        raise NotImplementedError()

    def change_photo(
        self, request: HttpRequest, user_id: int = Path(...), photo: UploadedFile = File(...)
    ) -> SuccessResponse:
        pass

    def change_email(
        self, request: HttpRequest, user_id: int = Path(...), body: EmailIn = Body(...)
    ) -> SuccessResponse:
        raise NotImplementedError()

    def rename_user(self, request: HttpRequest, user_id: int = Path(...), body: NameIn = Body(...)) -> SuccessResponse:
        raise NotImplementedError()
