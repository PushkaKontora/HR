from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.http import HttpRequest
from ninja import Body, File, Path, UploadedFile
from ninja.responses import Response

from api.internal.errors import BadRequestError, ForbiddenError, NotFoundError, UnauthorizedError
from api.internal.responses import SuccessResponse
from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    EmailIn,
    JWTTokens,
    NameIn,
    Payload,
    PhotoOut,
    RegistrationIn,
    ResettingPasswordIn,
    TokenType,
    UpdatingPasswordOut,
    UserOut,
)
from api.internal.v1.users.presentation.errors import (
    EmailHasAlreadyRegisteredError,
    EmailIsAlreadyRegisteredError,
    FileIsNotImageError,
    PasswordsDoNotMatchError,
    UserIsLeaderOfDepartmentError,
)
from api.internal.v1.users.presentation.routers import IAuthHandlers, IUserHandlers
from api.logging import get_logger
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
    def authorize(self, user: User, user_id: int) -> bool:
        pass

    @abstractmethod
    def match_passwords(self, user_id: int, body: ResettingPasswordIn) -> bool:
        pass

    @abstractmethod
    def reset(self, user_id: int, body: ResettingPasswordIn) -> UpdatingPasswordOut:
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


class IJWTService(ABC):
    @abstractmethod
    def try_get_user(self, payload: Payload) -> Optional[User]:
        pass

    @abstractmethod
    def create_tokens(self, user: User) -> JWTTokens:
        pass

    @abstractmethod
    def get_tokens(self, tokens: JWTTokens) -> AuthenticationOut:
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

    @abstractmethod
    def exists_user_with_id(self, user_id: int) -> bool:
        pass


class IPhotoService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, user_id: int) -> bool:
        pass

    @abstractmethod
    def upload(self, user_id: int, photo: UploadedFile) -> PhotoOut:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    def is_image(self, photo: UploadedFile) -> bool:
        pass


class AuthHandlers(IAuthHandlers):
    REFRESH_TOKEN_IS_NOT_IN_COOKIES = "Refresh token is not in cookies"
    INVALID_SIGNATURE_OR_PAYLOAD = "Invalid signature or payload"
    TOKEN_IS_EXPIRED = "The token is expired"
    TOKEN_WAS_NOT_ISSUED = "The token was not issued"
    TOKEN_IS_REVOKED = "The token is revoked"

    def __init__(
        self,
        registration_service: IRegistrationService,
        auth_service: IAuthenticationService,
        jwt_service: IJWTService,
        resetting_password_service: IResettingPasswordService,
        getting_user_service: IGettingUserService,
    ):
        self.getting_user_service = getting_user_service
        self.resetting_password_service = resetting_password_service
        self.jwt_service = jwt_service
        self.auth_service = auth_service
        self.registration_service = registration_service

    def register_user(self, request: HttpRequest, body: RegistrationIn = Body(...)) -> SuccessResponse:
        if self.registration_service.is_email_taken(body.email):
            raise EmailHasAlreadyRegisteredError()

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
        self, request: HttpRequest, user_id: int = Path(...), body: ResettingPasswordIn = Body(...)
    ) -> UpdatingPasswordOut:
        if not self.getting_user_service.exists_user_with_id(user_id):
            raise NotFoundError()

        if not self.resetting_password_service.authorize(request.user, user_id):
            raise ForbiddenError()

        if not self.resetting_password_service.match_passwords(user_id, body):
            raise PasswordsDoNotMatchError()

        return self.resetting_password_service.reset(user_id, body)

    def get_response_with_tokens(self, user: User) -> Response:
        tokens = self.jwt_service.create_tokens(user)

        response = Response(self.jwt_service.get_tokens(tokens))
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
        photo_service: IPhotoService,
    ):
        self.photo_service = photo_service
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
        auth_user: User = request.user
        logger = get_logger(request)

        logger.info(
            "Deleting a user id={user_id} auth_user={auth_user}".format(
                user_id=user_id,
                auth_user={"id": auth_user.id, "is_department_leader": hasattr(auth_user, "department")},
            )
        )

        logger.info("Checking the existence of the user...")
        if not self.getting_user_service.exists_user_with_id(user_id):
            logger.success("Not found the user")
            raise NotFoundError()

        logger.info("Authorization...")
        if not self.deleting_user_service.authorize(auth_user, user_id):
            logger.success("Permission denied")
            raise ForbiddenError()

        logger.info("Checking an existence of leadership of the user...")
        if self.deleting_user_service.is_user_leader_of_department(user_id):
            logger.success("The user is leader of department")
            raise UserIsLeaderOfDepartmentError()

        logger.info("Deleting the user...")
        self.deleting_user_service.delete(user_id)
        logger.success("The user was deleted")

        return SuccessResponse()

    def upload_photo(self, request: HttpRequest, user_id: int = Path(...), photo: UploadedFile = File(...)) -> PhotoOut:
        auth_user: User = request.user
        logger = get_logger(request)

        logger.info(
            "Uploading a photo user_id={user_id} auth_user={auth_user} photo={photo}".format(
                user_id=user_id,
                auth_user={"id": auth_user.id, "has_photo": bool(auth_user.photo)},
                photo={"name": photo.name, "content_type": photo.content_type, "size": photo.size},
            )
        )

        logger.info("Checking the existence of the user...")
        if not self.getting_user_service.exists_user_with_id(user_id):
            logger.success("Not found the user")
            raise NotFoundError()

        logger.info("Authorization...")
        if not self.photo_service.authorize(auth_user, user_id):
            logger.success("Permission denied")
            raise ForbiddenError()

        logger.info("Checking the file...")
        if not self.photo_service.is_image(photo):
            logger.success("The file is not image")
            raise FileIsNotImageError()

        logger.info("Uploading the photo...")
        photo_out = self.photo_service.upload(user_id, photo)
        logger.success("The photo was uploaded")

        return photo_out

    def delete_photo(self, request: HttpRequest, user_id: int = Path(...)) -> SuccessResponse:
        auth_user: User = request.user
        logger = get_logger(request)

        logger.info(
            "Deleting a photo user_id={user_id} auth_user={auth_user}".format(
                user_id=user_id,
                auth_user={"id": auth_user.id, "has_photo": bool(auth_user.photo)},
            )
        )

        logger.info("Checking the existence of the user...")
        if not self.getting_user_service.exists_user_with_id(user_id):
            logger.success("Not found the user")
            raise NotFoundError()

        logger.info("Authorization...")
        if not self.photo_service.authorize(auth_user, user_id):
            logger.success("Permission denied")
            raise ForbiddenError()

        logger.info("Deleting the photo...")
        self.photo_service.delete(user_id)
        logger.success("The user photo was deleted")

        return SuccessResponse()

    def change_email(
        self, request: HttpRequest, user_id: int = Path(...), body: EmailIn = Body(...)
    ) -> SuccessResponse:
        if not self.getting_user_service.exists_user_with_id(user_id):
            raise NotFoundError()

        if not self.changing_email_service.authorize(request.user, user_id):
            raise ForbiddenError()

        if self.changing_email_service.is_email_already_registered(body):
            raise EmailIsAlreadyRegisteredError()

        self.changing_email_service.change_email(user_id, body)

        return SuccessResponse()

    def rename_user(self, request: HttpRequest, user_id: int = Path(...), body: NameIn = Body(...)) -> SuccessResponse:
        if not self.getting_user_service.exists_user_with_id(user_id):
            raise NotFoundError()

        if not self.renaming_user_service.authorize(request.user, user_id):
            raise ForbiddenError()

        self.renaming_user_service.rename(user_id, body)

        return SuccessResponse()
