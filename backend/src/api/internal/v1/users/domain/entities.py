from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import EmailStr, HttpUrl

from api.internal.models import Permissions

PDF_RE = r"([^\\s]+(\\.(?i)(pdf))$)"


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


class UserResumeOut(Schema):
    id: int


class UserDepartmentOut(Schema):
    id: int


class PasswordOut(Schema):
    updated_at: datetime


class UserOut(Schema):
    id: int
    email: EmailStr
    permission: Permissions
    surname: str
    name: str
    patronymic: str
    photo: str
    resume: Optional[UserResumeOut]
    department: Optional[UserDepartmentOut]
    password: PasswordOut


class EmailIn(Schema):
    email: EmailStr


class NameIn(Schema):
    surname: str
    name: str
    patronymic: str


class ResetPasswordIn(Schema):
    previous_password: str
    new_password: str


class ResetPasswordOut(Schema):
    updated_at: datetime


class PhotoOut(Schema):
    photo: HttpUrl
