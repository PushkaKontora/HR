from abc import ABC, abstractmethod

from django.db.transaction import atomic

from api.internal.v1.users.domain.entities import RegistrationIn
from api.internal.v1.users.presentation.handlers import IRegistrationService
from api.models import Password, User


class IUserRepository(ABC):
    @abstractmethod
    def exists_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def create(self, email: str, surname: str, name: str, patronymic: str) -> User:
        pass


class IPasswordRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, password: str) -> Password:
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
