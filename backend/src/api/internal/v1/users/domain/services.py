import uuid
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from bcrypt import checkpw
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.transaction import atomic
from django.utils.timezone import now
from jwt import PyJWTError, decode, encode
from ninja import UploadedFile
from pydantic import ValidationError

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
from api.internal.v1.users.domain.utils import get_photo_filename, hash_password
from api.internal.v1.users.presentation.handlers import (
    IAuthenticationService,
    IChangingEmailService,
    IDeletingUserService,
    IGettingUserService,
    IJWTService,
    IPhotoService,
    IRegistrationService,
    IRenamingUserService,
    IResettingPasswordService,
)
from api.models import IssuedToken, Password, Permission, User


class IUserRepository(ABC):
    @abstractmethod
    def exists_user_with_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def create(self, email: str, surname: str, name: str, patronymic: str) -> User:
        pass

    @abstractmethod
    def try_get_user_with_email_and_password(self, email: str, password: str) -> Optional[User]:
        pass

    @abstractmethod
    def try_get_user_with_resume_department_and_password_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def try_get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_for_update_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def exists_user_with_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass


class IPasswordRepository(ABC):
    @abstractmethod
    def create(self, owner_id: int, password: str) -> Password:
        pass

    @abstractmethod
    def get_password_value_by_user_id(self, owner_id: int) -> Password:
        pass

    @abstractmethod
    def get_password_for_update_by_user_id(self, owner_id: int) -> Password:
        pass


class IIssuedTokenRepository(ABC):
    @abstractmethod
    def revoke_all_tokens_for_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_or_create(self, user_id, value: str) -> IssuedToken:
        pass

    @abstractmethod
    def try_get_ony(self, value: str) -> Optional[IssuedToken]:
        pass


class IDepartmentRepository(ABC):
    @abstractmethod
    def is_leader(self, user_id: int) -> bool:
        pass


class RegistrationService(IRegistrationService):
    def __init__(self, user_repo: IUserRepository, password_repo: IPasswordRepository):
        self.password_repo = password_repo
        self.user_repo = user_repo

    def is_email_taken(self, email: str) -> bool:
        return self.user_repo.exists_user_with_email(email)

    @atomic
    def register(self, body: RegistrationIn) -> None:
        user = self.user_repo.create(body.email, body.surname, body.name, body.patronymic)

        self.password_repo.create(user.id, hash_password(body.password))


class AuthenticationService(IAuthenticationService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authenticate(self, body: AuthenticationIn) -> Optional[User]:
        return self.user_repo.try_get_user_with_email_and_password(body.email, body.password)


class JWTService(IJWTService):
    ALGORITHMS = ["HS256"]

    def __init__(self, issued_token_repo: IIssuedTokenRepository, user_repo: IUserRepository):
        self.user_repo = user_repo
        self.issued_token_repo = issued_token_repo

    def try_get_user(self, payload: Payload) -> Optional[User]:
        return self.user_repo.try_get_user_by_id(payload.user_id)

    def try_get_payload(self, value: str) -> Optional[Payload]:
        try:
            return Payload.from_dict(decode(value, settings.SECRET_KEY, algorithms=self.ALGORITHMS))
        except (PyJWTError, ValidationError):
            return None

    def is_type(self, payload: Payload, token_type: TokenType) -> bool:
        return payload.type == token_type

    def is_token_expired(self, payload: Payload) -> bool:
        return int(now().timestamp()) >= payload.expires_in

    def try_get_issued_token(self, value: str) -> Optional[IssuedToken]:
        return self.issued_token_repo.try_get_ony(value)

    def revoke_all_issued_tokens_for_user(self, owner: User) -> None:
        self.issued_token_repo.revoke_all_tokens_for_user(owner.id)

    def create_tokens(self, user: User) -> JWTTokens:
        tokens = JWTTokens.create(
            self.generate_token(user, TokenType.ACCESS, settings.ACCESS_TOKEN_TTL),
            self.generate_token(user, TokenType.REFRESH, settings.REFRESH_TOKEN_TTL),
        )

        with atomic():
            self.issued_token_repo.revoke_all_tokens_for_user(user.id)
            self.issued_token_repo.get_or_create(user.id, tokens.refresh)

        return tokens

    def get_tokens(self, tokens: JWTTokens) -> AuthenticationOut:
        return AuthenticationOut.from_tokens(tokens)

    def generate_token(self, user: User, token_type: TokenType, ttl: timedelta) -> str:
        payload = Payload.create(
            token_type,
            user.id,
            Permission(user.permission),
            int((now() + ttl).timestamp()),
        )

        return encode(payload.dict(), settings.SECRET_KEY, algorithm=self.ALGORITHMS[0])


class GettingUserService(IGettingUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def try_get_user(self, user_id: int) -> Optional[UserOut]:
        user = self.user_repo.try_get_user_with_resume_department_and_password_by_id(user_id)

        if not user:
            return None

        return UserOut.from_user(user)

    def exists_user_with_id(self, user_id: int) -> bool:
        return self.user_repo.exists_user_with_id(user_id)


class ResettingPasswordService(IResettingPasswordService):
    def __init__(self, password_repo: IPasswordRepository):
        self.password_repo = password_repo

    def authorize(self, user: User, user_id: int) -> bool:
        return user.id == user_id

    def match_passwords(self, user_id: int, body: ResettingPasswordIn) -> bool:
        password = self.password_repo.get_password_value_by_user_id(user_id)

        return checkpw(body.previous_password.encode(), password.value.encode())

    def reset(self, user_id: int, body: ResettingPasswordIn) -> UpdatingPasswordOut:
        password = self.password_repo.get_password_for_update_by_user_id(user_id)

        password.value = hash_password(body.new_password)
        password.save(update_fields=["value", "updated_at"])

        return UpdatingPasswordOut.from_password(password)


class DeletingUserService(IDeletingUserService):
    def __init__(self, user_repo: IUserRepository, department_repo: IDepartmentRepository):
        self.user_repo = user_repo
        self.department_repo = department_repo

    def authorize(self, auth_user: User, user_id: int) -> bool:
        return auth_user.id == user_id

    def is_user_leader_of_department(self, user_id: int) -> bool:
        return self.department_repo.is_leader(user_id)

    @atomic
    def delete(self, user_id: int) -> None:
        user = self.user_repo.get_user_for_update_by_id(user_id)

        user.delete()


class RenamingUserService(IRenamingUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authorize(self, auth_user: User, user_id: int) -> bool:
        return auth_user.id == user_id

    @atomic
    def rename(self, user_id: int, body: NameIn) -> None:
        user = self.user_repo.get_user_for_update_by_id(user_id)

        user.surname = body.surname
        user.name = body.name
        user.patronymic = body.patronymic
        user.save(update_fields=["surname", "name", "patronymic"])


class ChangingEmailService(IChangingEmailService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authorize(self, auth_user: User, user_id: int) -> bool:
        return auth_user.id == user_id

    def is_email_already_registered(self, body: EmailIn) -> bool:
        return self.user_repo.exists_user_with_email(body.email)

    @atomic
    def change_email(self, user_id: int, body: EmailIn) -> None:
        user = self.user_repo.get_user_for_update_by_id(user_id)

        user.email = body.email
        user.save(update_fields=["email"])


class PhotoService(IPhotoService):
    PHOTO_MIME_TYPES = ("image/png", "image/jpeg")

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authorize(self, auth_user: User, user_id: int) -> bool:
        return auth_user.id == user_id

    def upload(self, user_id: int, photo: UploadedFile) -> PhotoOut:
        with atomic():
            user = self.user_repo.get_user_for_update_by_id(user_id)
            previous_name = user.photo.name if user.photo else None

            user.photo = UploadedFile(photo, get_photo_filename(photo, user_id))
            user.save(update_fields=["photo"])

        if previous_name is not None:
            default_storage.delete(previous_name)

        return PhotoOut.from_user(user)

    @atomic
    def delete(self, user_id: int) -> None:
        user = self.user_repo.get_user_for_update_by_id(user_id)

        user.photo.delete(save=True)

    def is_image(self, photo: UploadedFile) -> bool:
        return photo.content_type in self.PHOTO_MIME_TYPES
