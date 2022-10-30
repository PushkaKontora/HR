from abc import ABC, abstractmethod
from typing import List, Optional

from django.db.models import QuerySet

from api.internal.v1.departments.domain.entities import DepartmentOut, LeaderOut
from api.internal.v1.departments.presentation.handlers import IGettingService
from api.models import Department


class IDepartmentRepository(ABC):
    @abstractmethod
    def try_get_one_with_leader(self, department_id: int) -> Optional[Department]:
        pass

    @abstractmethod
    def get_all(self) -> QuerySet[Department]:
        pass


class GettingService(IGettingService):
    def __init__(self, department_repo: IDepartmentRepository):
        self.department_repo = department_repo

    def try_get_one_department_out(self, department_id: int) -> Optional[DepartmentOut]:
        department = self.department_repo.try_get_one_with_leader(department_id)

        if not department:
            return None

        return self.get_department_out(department)

    def get_many_department_out(self) -> List[DepartmentOut]:
        return [self.get_department_out(department) for department in self.department_repo.get_all()]

    @staticmethod
    def get_department_out(department: Department) -> DepartmentOut:
        leader = department.leader
        return DepartmentOut(
            id=department.id,
            name=department.name,
            description=department.description,
            vacancies_amount=department.vacancies.count(),
            leader=LeaderOut(id=leader.id, surname=leader.surname, name=leader.name, patronymic=leader.patronymic),
        )
