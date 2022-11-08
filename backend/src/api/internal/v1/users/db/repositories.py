from typing import Optional

from api.internal.v1.users.domain.services import (
    IDepartmentRepository,
    IIssuedTokenRepository,
    IPasswordRepository,
    IUserRepository,
)
from api.internal.v1.users.domain.utils import hash_password
from api.models import Department, IssuedToken, Password, User


class UserRepository(IUserRepository):
    def try_get_user_with_email_and_password(self, email: str, password: str) -> Optional[User]:
        return User.objects.filter(email=email, password__value=hash_password(password)).first()

    def try_get_user_with_resume_department_and_password_by_id(self, user_id: int) -> Optional[User]:
        return User.objects.select_related("resume", "department", "password").filter(id=user_id).first()

    def try_get_user_by_id(self, user_id: int) -> Optional[User]:
        return User.objects.filter(id=user_id).first()

    def get_user_for_update(self, user_id: int) -> User:
        return User.objects.select_for_update().get(id=user_id)

    def get_user_by_id(self, user_id: int) -> User:
        return User.objects.get(id=user_id)

    def exists_user_with_email(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def create(self, email: str, surname: str, name: str, patronymic: str) -> User:
        return User.objects.create(email=email, surname=surname, name=name, patronymic=patronymic)

    def exists_user_with_id(self, user_id: int) -> bool:
        return User.objects.filter(id=user_id).exists()


class PasswordRepository(IPasswordRepository):
    def create(self, user_id: int, password: str) -> Password:
        return Password.objects.create(owner_id=user_id, value=password)


class IssuedTokenRepository(IIssuedTokenRepository):
    def revoke_all_tokens_for_user(self, user_id: int) -> None:
        IssuedToken.objects.filter(owner_id=user_id).update(revoked=True)

    def get_or_create(self, user_id, value: str) -> IssuedToken:
        return IssuedToken.objects.get_or_create(owner_id=user_id, value=value)[0]

    def try_get_ony(self, value: str) -> Optional[IssuedToken]:
        return IssuedToken.objects.filter(value=value).first()


class DepartmentRepository(IDepartmentRepository):
    def is_leader(self, user_id: int) -> bool:
        return Department.objects.filter(leader_id=user_id).exists()
