from datetime import datetime
from typing import Optional

from ninja import UploadedFile
from pydantic import EmailStr

from api.internal.base import BaseSchema

PDF_RE = r"([^\\s]+(\\.(?i)(pdf))$)"


class RegistrationIn(BaseSchema):
    email: EmailStr
    password: str
    surname: str
    name: str
    patronymic: str


class AuthenticationIn(BaseSchema):
    email: EmailStr
    password: str


class AuthenticationOut(BaseSchema):
    access_token: str


class UserResumeOut(BaseSchema):
    id: int


class UserDepartmentOut(BaseSchema):
    id: int


class UserOut(BaseSchema):
    id: int
    email: EmailStr
    permission: str
    surname: str
    name: str
    patronymic: str
    photo: str
    resume: Optional[UserResumeOut]
    department: Optional[UserDepartmentOut]


class EmailIn(BaseSchema):
    email: EmailStr


class NameIn(BaseSchema):
    surname: str
    name: str
    patronymic: str


class ResetPasswordIn(BaseSchema):
    previous_password: str
    new_password: str


class ResetPasswordOut(BaseSchema):
    updated_at: datetime
