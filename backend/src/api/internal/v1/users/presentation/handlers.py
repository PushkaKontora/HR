from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.http import HttpRequest
from ninja import Body, File, Path, UploadedFile
from ninja.responses import Response

from api.internal.v1.exceptions import BadRequestError, ForbiddenError, NotFoundError, UnauthorizedError
from api.internal.v1.responses import SuccessResponse
from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    EmailIn,
    NameIn,
    PasswordUpdatedAtOut,
    Payload,
    RegistrationIn,
    ResetPasswordIn,
    Tokens,
    TokenType,
    UserOut,
)
from api.internal.v1.users.presentation.exceptions import (
    EmailIsAlreadyRegisteredError,
    PasswordDoesNotMatchError,
    PasswordHasAlreadyRegisteredError,
    UserIsLeaderOfDepartmentError,
)
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


class IResettingPasswordService(ABC):
    @abstractmethod
    def authorize_only_self(self, user: User, user_id: int) -> bool:
        pass

    @abstractmethod
    def match_password(self, user: User, body: ResetPasswordIn) -> bool:
        pass

    @abstractmethod
    def reset(self, user: User, body: ResetPasswordIn) -> PasswordUpdatedAtOut:
        pass


class IDeletingUserService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, user_id: int) -> bool:
        pass

    @abstractmethod
    def is_user_leader_of_department(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass


class IRenamingUserService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, user_id: int) -> bool:
        pass

    @abstractmethod
    def rename(self, user_id: int, body: NameIn) -> None:
        pass


class IChangingEmailService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, user_id: int) -> bool:
        pass

    @abstractmethod
    def is_email_already_registered(self, body: EmailIn) -> bool:
        pass

    @abstractmethod
    def change_email(self, user_id: int, body: EmailIn) -> None:
        pass


class IJWTService(ABC, metaclass=ABCMeta):
    @abstractmethod
    def try_get_user(self, payload: Payload) -> Optional[User]:
        pass

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


class IGettingUserService(ABC):
    @abstractmethod
    def try_get_user(self, user_id: int) -> Optional[UserOut]:
        pass


class AuthHandlers(IAuthHandlers):
    REFRESH_TOKEN_IS_NOT_IN_COOKIES = "Refresh token is not in cookies"
    INVALID_SIGNATURE_OR_PAYLOAD = "Invalid signature or payload"
    TOKEN_IS_EXPIRED = "The token is expired"
    TOKEN_WAS_NOT_ISSUED = "The token was not issued"
    TOKEN_IS_REVOKED = "The token is revoked"

    ONLY_SELF = "Only self"

    def __init__(
        self,
        registration_service: IRegistrationService,
        auth_service: IAuthenticationService,
        jwt_service: IJWTService,
        resetting_password_service: IResettingPasswordService,
    ):
        self.resetting_password_service = resetting_password_service
        self.jwt_service = jwt_service
        self.auth_service = auth_service
        self.registration_service = registration_service

    def register_user(self, request: HttpRequest, body: RegistrationIn = Body(...)) -> SuccessResponse:
        if self.registration_service.is_email_taken(body.email):
            raise PasswordHasAlreadyRegisteredError()

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
    ) -> PasswordUpdatedAtOut:
        if not self.resetting_password_service.authorize_only_self(request.user, user_id):
            raise ForbiddenError(self.ONLY_SELF)

        if not self.resetting_password_service.match_password(request.user, body):
            raise PasswordDoesNotMatchError()

        return self.resetting_password_service.reset(request.user, body)

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
    def __init__(
        self,
        getting_user_service: IGettingUserService,
        deleting_user_service: IDeletingUserService,
        renaming_user_service: IRenamingUserService,
        changing_email_service: IChangingEmailService,
    ):
        self.changing_email_service = changing_email_service
        self.getting_user_service = getting_user_service
        self.deleting_user_service = deleting_user_service
        self.renaming_user_service = renaming_user_service

    def get_user(self, request: HttpRequest, user_id: int = Path(...)) -> UserOut:
        user_out = self.getting_user_service.try_get_user(user_id)

        if not user_out:
            raise NotFoundError()

        return user_out

    def delete_user(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        if not self.deleting_user_service.authorize(request.user, user_id):
            raise ForbiddenError()

        if self.deleting_user_service.is_user_leader_of_department(user_id):
            raise UserIsLeaderOfDepartmentError()

        self.deleting_user_service.delete(user_id)

        return SuccessResponse()

    def change_photo(
        self, request: HttpRequest, user_id: int = Path(...), photo: UploadedFile = File(...)
    ) -> SuccessResponse:
        raise NotImplementedError()

    def remove_photo(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        raise NotImplementedError()

    def change_email(
        self, request: HttpRequest, user_id: int = Path(...), body: EmailIn = Body(...)
    ) -> SuccessResponse:
        if not self.changing_email_service.authorize(request.user, user_id):
            raise ForbiddenError()

        if self.changing_email_service.is_email_already_registered(body):
            raise EmailIsAlreadyRegisteredError()

        self.changing_email_service.change_email(user_id, body)

        return SuccessResponse()

    def rename_user(self, request: HttpRequest, user_id: int = Path(...), body: NameIn = Body(...)) -> SuccessResponse:
        if not self.renaming_user_service.authorize(request.user, user_id):
            raise ForbiddenError()

        self.renaming_user_service.rename(user_id, body)

        return SuccessResponse()
