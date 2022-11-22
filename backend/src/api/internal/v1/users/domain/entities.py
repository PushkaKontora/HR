from datetime import datetime
from enum import Enum
from typing import Optional

from ninja import Schema
from pydantic import AnyHttpUrl, EmailStr, HttpUrl, validator

from api.models import Password, Permission, User

PDF_RE = r"([^\\s]+(\\.(?i)(pdf))$)"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class RegistrationIn(Schema):
    email: EmailStr
    password: str
    surname: str
    name: str
    patronymic: str


class AuthenticationIn(Schema):
    email: EmailStr
    password: str


class AuthenticationOut(Schema):
    access_token: str

    @staticmethod
    def from_tokens(tokens: "JWTTokens") -> "AuthenticationOut":
        return AuthenticationOut(access_token=tokens.access)


class UserResumeOut(Schema):
    id: int


class UserDepartmentOut(Schema):
    id: int


class PasswordOut(Schema):
    updated_at: datetime


class UserOut(Schema):
    id: int
    email: EmailStr
    permission: Permission
    surname: str
    name: str
    patronymic: str
    photo: Optional[AnyHttpUrl]
    resume: Optional[UserResumeOut]
    department: Optional[UserDepartmentOut]
    password: PasswordOut

    @staticmethod
    def from_user(user: User) -> "UserOut":
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


class EmailIn(Schema):
    email: EmailStr


class NameIn(Schema):
    surname: str
    name: str
    patronymic: str


class ResettingPasswordIn(Schema):
    previous_password: str
    new_password: str

    @validator("new_password")
    @classmethod
    def validate_not_equality_of_passwords(cls, field_value, values, field, config):
        if field_value == values["previous_password"]:
            raise ValueError("The passwords must be unique")

        return field_value


class UpdatingPasswordOut(Schema):
    updated_at: datetime

    @staticmethod
    def from_password(password: Password) -> "UpdatingPasswordOut":
        return UpdatingPasswordOut(updated_at=password.updated_at)


class PhotoOut(Schema):
    photo: AnyHttpUrl

    @staticmethod
    def from_user(user: User) -> "PhotoOut":
        return PhotoOut(photo=user.photo.url)


class JWTTokens(Schema):
    access: str
    refresh: str

    @staticmethod
    def create(access: str, refresh: str) -> "JWTTokens":
        return JWTTokens(access=access, refresh=refresh)


class Payload(Schema):
    type: TokenType
    user_id: int
    permission: Permission
    expires_in: int

    @staticmethod
    def from_dict(dictionary_payload: dict) -> "Payload":
        return Payload(**dictionary_payload)

    @staticmethod
    def create(token_type: TokenType, user_id: int, permission: Permission, expires_in: int) -> "Payload":
        return Payload(type=token_type, user_id=user_id, permission=permission, expires_in=expires_in)
