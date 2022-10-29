from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from bcrypt import checkpw
from django.conf import settings
from django.db.transaction import atomic
from django.utils.timezone import now
from jwt import PyJWTError, decode, encode
from pydantic import ValidationError

from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    PasswordOut,
    PasswordUpdatedAtOut,
    Payload,
    RegistrationIn,
    ResetPasswordIn,
    Tokens,
    TokenType,
    UserDepartmentOut,
    UserOut,
    UserResumeOut,
)
from api.internal.v1.users.domain.utils import hash_password
from api.internal.v1.users.presentation.handlers import (
    IAuthenticationService,
    IDeleteUserService,
    IJWTService,
    IRegistrationService,
    IResetPasswordService,
    IUserService,
)
from api.models import IssuedToken, Password, User


class IUserRepository(ABC):
    @abstractmethod
    def exists_email(self, email: str) -> bool:
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
    def get_for_update(self, user_id: int) -> User:
        pass


class IPasswordRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, password: str) -> Password:
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
        return self.user_repo.exists_email(email)

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
            return Payload(**decode(value, settings.SECRET_KEY, algorithms=self.ALGORITHMS))
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

    def create_tokens(self, user: User) -> Tokens:
        tokens = Tokens(
            access=self.generate_token(user, TokenType.ACCESS, settings.ACCESS_TOKEN_TTL),
            refresh=self.generate_token(user, TokenType.REFRESH, settings.REFRESH_TOKEN_TTL),
        )

        with atomic():
            self.issued_token_repo.revoke_all_tokens_for_user(user.id)
            self.issued_token_repo.get_or_create(user.id, tokens.refresh)

        return tokens

    def get_tokens_out(self, tokens: Tokens) -> AuthenticationOut:
        return AuthenticationOut(access_token=tokens.access)

    def generate_token(self, user: User, token_type: TokenType, ttl: timedelta) -> str:
        payload = Payload(
            type=token_type.value,
            user_id=user.id,
            permission=str(user.permission),
            expires_in=int((now() + ttl).timestamp()),
        )

        return encode(payload.dict(), settings.SECRET_KEY, algorithm=self.ALGORITHMS[0])


class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def try_get_user(self, user_id: int) -> Optional[UserOut]:
        user = self.user_repo.try_get_user_with_resume_department_and_password_by_id(user_id)

        if not user:
            return None

        return UserOut(
            id=user.id,
            email=user.email,
            permission=user.permission,
            surname=user.surname,
            name=user.name,
            patronymic=user.patronymic,
            photo=user.photo.url if user.photo else None,
            resume=UserResumeOut.from_orm(user.resume) if hasattr(user, "resume") else None,
            department=UserDepartmentOut.from_orm(user.department) if hasattr(user, "department") else None,
            password=PasswordOut.from_orm(user.password),
        )


class ResetPasswordService(IResetPasswordService):
    def authorize_only_self(self, user: User, user_id: int) -> bool:
        return user.id == user_id

    def match_password(self, user: User, body: ResetPasswordIn) -> bool:
        return checkpw(body.previous_password.encode(), user.password.value.encode())

    def reset(self, user: User, body: ResetPasswordIn) -> PasswordUpdatedAtOut:
        password = user.password
        password.value = hash_password(body.new_password)
        password.save(update_fields=["value", "updated_at"])

        return PasswordUpdatedAtOut(updated_at=password.updated_at)


class DeleteUserService(IDeleteUserService):
    def __init__(self, user_repo: IUserRepository, department_repo: IDepartmentRepository):
        self.user_repo = user_repo
        self.department_repo = department_repo

    def authorize(self, auth_user: User, user_id: int) -> bool:
        return auth_user.id == user_id

    def is_user_leader_of_department(self, user_id: int) -> bool:
        return self.department_repo.is_leader(user_id)

    @atomic
    def delete(self, user_id: int) -> None:
        user = self.user_repo.get_for_update(user_id)

        user.delete()
