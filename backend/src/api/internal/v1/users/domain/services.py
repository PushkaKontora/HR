from abc import ABC, abstractmethod
from datetime import timedelta
from enum import Enum
from typing import Optional

from django.conf import settings
from django.db.transaction import atomic
from django.utils.timezone import now
from jwt import encode

from api.internal.v1.users.domain.entities import AuthenticationIn, AuthenticationOut, Payload, RegistrationIn, Tokens
from api.internal.v1.users.presentation.handlers import IAuthenticationService, IRegistrationService
from api.models import IssuedToken, Password, User


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class IUserRepository(ABC):
    @abstractmethod
    def exists_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def create(self, email: str, surname: str, name: str, patronymic: str) -> User:
        pass

    @abstractmethod
    def try_get_user_with_email_and_password(self, email: str, password: str) -> User:
        pass


class IPasswordRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, password: str) -> Password:
        pass


class IIssuedTokenRepository(ABC):
    @abstractmethod
    def revoke_all_tokens_from_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_or_create(self, user_id, value: str) -> IssuedToken:
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

        self.password_repo.create(user.id, body.password)


class AuthenticationService(IAuthenticationService):
    def __init__(self, user_repo: IUserRepository, issued_token_repo: IIssuedTokenRepository):
        self.issued_token_repo = issued_token_repo
        self.user_repo = user_repo

    def authenticate(self, body: AuthenticationIn) -> Optional[Tokens]:
        user = self.user_repo.try_get_user_with_email_and_password(body.email, body.password)

        if not user:
            return None

        tokens = Tokens(
            access=self.generate_token(user, TokenType.ACCESS, settings.ACCESS_TOKEN_TTL),
            refresh=self.generate_token(user, TokenType.REFRESH, settings.REFRESH_TOKEN_TTL),
        )

        with atomic():
            self.issued_token_repo.revoke_all_tokens_from_user(user.id)
            self.issued_token_repo.get_or_create(user.id, tokens.refresh)

        return tokens

    def get_authentication_out(self, tokens: Tokens) -> AuthenticationOut:
        return AuthenticationOut(access_token=tokens.access)

    @staticmethod
    def generate_token(user: User, token_type: TokenType, ttl: timedelta) -> str:
        payload = Payload(
            type=token_type.value, user_id=user.id, permission=str(user.permission), exp=int((now() + ttl).timestamp())
        )

        return encode(payload.dict(), settings.SECRET_KEY)
