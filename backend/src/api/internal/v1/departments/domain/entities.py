from typing import Optional

from ninja import Schema

from api.models import Department


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

    @staticmethod
    def from_department(department: Department) -> "DepartmentOut":
        leader = department.leader
        return DepartmentOut(
            id=department.id,
            name=department.name,
            description=department.description,
            vacancies_amount=department.vacancies.count(),
            leader=LeaderOut(id=leader.id, surname=leader.surname, name=leader.name, patronymic=leader.patronymic),
        )
