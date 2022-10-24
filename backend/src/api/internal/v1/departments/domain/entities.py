from ninja import Schema
from pydantic import EmailStr


class LeaderOut(Schema):
    id: int
    surname: str
    name: str
    patronymic: str
    email: EmailStr


class DepartmentOut(Schema):
    id: int
    name: str
    description: str
    vacancies_amount: int
    leader: LeaderOut
