import bcrypt
from bcrypt import hashpw
from django.conf import settings

from api.internal.v1.users.domain.services import IPasswordRepository, IUserRepository
from api.models import Password, User


class UserRepository(IUserRepository):
    def exists_email(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def create(self, email: str, surname: str, name: str, patronymic: str) -> User:
        return User.objects.create(email=email, surname=surname, name=name, patronymic=patronymic)


class PasswordRepository(IPasswordRepository):
    def create(self, user_id: int, password: str) -> Password:
        return Password.objects.create(owner_id=user_id, value=hashpw(password.encode("utf-8"), settings.SALT).decode())
