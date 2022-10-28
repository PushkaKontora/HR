from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from django.conf import settings
from django.db.transaction import atomic
from django.utils.timezone import now
from jwt import PyJWTError, decode, encode
from pydantic import ValidationError

from api.internal.v1.users.domain.entities import (
    AuthenticationIn,
    AuthenticationOut,
    Payload,
    RegistrationIn,
    Tokens,
    TokenType,
)
from api.internal.v1.users.presentation.handlers import IAuthenticationService, IJWTService, IRegistrationService
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
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authenticate(self, body: AuthenticationIn) -> Optional[User]:
        return self.user_repo.try_get_user_with_email_and_password(body.email, body.password)


class JWTService(IJWTService):
    ALGORITHMS = ["HS256"]

    def __init__(self, issued_token_repo: IIssuedTokenRepository):
        self.issued_token_repo = issued_token_repo

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
