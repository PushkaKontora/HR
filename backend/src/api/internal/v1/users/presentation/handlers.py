from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.http import HttpRequest
from ninja import Body, File, Path, UploadedFile
from ninja.responses import Response

from api.internal.v1.exceptions import BadRequestError, UnauthorizedError
from api.internal.v1.responses import SuccessResponse
from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    EmailIn,
    NameIn,
    Payload,
    RegistrationIn,
    ResetPasswordIn,
    ResetPasswordOut,
    Tokens,
    TokenType,
    UserOut,
)
from api.internal.v1.users.presentation.exceptions import PasswordHasAlreadyRegistered
from api.internal.v1.users.presentation.routers import IAuthHandlers, IUserHandlers
from api.models import IssuedToken, User


class IRegistrationService(ABC):
    @abstractmethod
    def is_email_taken(self, email: str) -> bool:
        pass

    @abstractmethod
    def register(self, body: RegistrationIn) -> None:
        pass


class IAuthenticationService(ABC):
    @abstractmethod
    def authenticate(self, body: AuthenticationIn) -> Optional[User]:
        pass


class IJWTService(ABC):
    @abstractmethod
    def create_tokens(self, user: User) -> Tokens:
        pass

    @abstractmethod
    def get_tokens_out(self, tokens: Tokens) -> AuthenticationOut:
        pass

    @abstractmethod
    def try_get_payload(self, value: str) -> Optional[Payload]:
        pass

    @abstractmethod
    def is_type(self, payload: Payload, token_type: TokenType) -> bool:
        pass

    @abstractmethod
    def is_token_expired(self, payload: Payload) -> bool:
        pass

    @abstractmethod
    def try_get_issued_token(self, value: str) -> Optional[IssuedToken]:
        pass

    @abstractmethod
    def revoke_all_issued_tokens_for_user(self, owner: User) -> None:
        pass


class AuthHandlers(IAuthHandlers):
    REFRESH_TOKEN_IS_NOT_IN_COOKIES = "Refresh token is not in cookies"
    INVALID_SIGNATURE_OR_PAYLOAD = "Invalid signature or payload"
    TOKEN_IS_EXPIRED = "The token is expired"
    TOKEN_WAS_NOT_ISSUED = "The token was not issued"
    TOKEN_IS_REVOKED = "The token is revoked"

    def __init__(
        self, registration_service: IRegistrationService, auth_service: IAuthenticationService, jwt_service: IJWTService
    ):
        self.jwt_service = jwt_service
        self.auth_service = auth_service
        self.registration_service = registration_service

    def register_user(self, request: HttpRequest, body: RegistrationIn = Body(...)) -> SuccessResponse:
        if self.registration_service.is_email_taken(body.email):
            raise PasswordHasAlreadyRegistered()

        self.registration_service.register(body)

        return SuccessResponse()

    def authenticate_user(self, request: HttpRequest, body: AuthenticationIn = Body(...)) -> Response:
        user = self.auth_service.authenticate(body)

        if not user:
            raise UnauthorizedError()

        return self.get_response_with_tokens(user)

    def refresh_tokens(self, request: HttpRequest) -> Response:
        value: str = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE)

        if value is None:
            raise BadRequestError(self.REFRESH_TOKEN_IS_NOT_IN_COOKIES)

        payload = self.jwt_service.try_get_payload(value)

        if not payload or not self.jwt_service.is_type(payload, TokenType.REFRESH):
            raise BadRequestError(self.INVALID_SIGNATURE_OR_PAYLOAD)

        if self.jwt_service.is_token_expired(payload):
            raise BadRequestError(self.TOKEN_IS_EXPIRED)

        issued_token = self.jwt_service.try_get_issued_token(value)
        if not issued_token:
            raise BadRequestError(self.TOKEN_WAS_NOT_ISSUED)

        if issued_token.revoked:
            self.jwt_service.revoke_all_issued_tokens_for_user(issued_token.owner)
            raise BadRequestError(self.TOKEN_IS_REVOKED)

        return self.get_response_with_tokens(issued_token.owner)

    def reset_password(
        self, request: HttpRequest, user_id: int = Path(...), body: ResetPasswordIn = Body(...)
    ) -> ResetPasswordOut:
        raise NotImplementedError()

    def get_response_with_tokens(self, user: User) -> Response:
        tokens = self.jwt_service.create_tokens(user)

        response = Response(self.jwt_service.get_tokens_out(tokens))
        response.set_cookie(
            key=settings.REFRESH_TOKEN_COOKIE,
            value=tokens.refresh,
            httponly=True,
            expires=datetime.utcnow() + settings.REFRESH_TOKEN_TTL,
        )

        return response


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
