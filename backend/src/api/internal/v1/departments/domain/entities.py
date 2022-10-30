from typing import Optional

from ninja import Schema


class LeaderOut(Schema):
    id: int
    surname: str
    name: str
    patronymic: str


class DepartmentOut(Schema):
    id: int
    name: str
    description: Optional[str]
    vacancies_amount: int
    leader: LeaderOut
