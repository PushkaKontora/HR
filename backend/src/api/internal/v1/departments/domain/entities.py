from pydantic import EmailStr

from api.internal.base import BaseSchema


class LeaderOut(BaseSchema):
    id: int
    surname: str
    name: str
    patronymic: str
    email: EmailStr


class DepartmentOut(BaseSchema):
    id: int
    name: str
    description: str
    vacancies_amount: int
    leader: LeaderOut
