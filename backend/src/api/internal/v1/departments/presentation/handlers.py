from abc import ABC, abstractmethod
from typing import Iterable, Optional

from django.http import HttpRequest
from ninja import Path

from api.internal.v1.departments.domain.entities import DepartmentOut
from api.internal.v1.departments.presentation.routers import IDepartmentHandlers, IDepartmentsHandlers
from api.internal.v1.exceptions import NotFoundError


class IGettingService(ABC):
    @abstractmethod
    def try_get_one_department_out(self, department_id: int) -> Optional[DepartmentOut]:
        pass

    @abstractmethod
    def get_many_department_out(self) -> Iterable[DepartmentOut]:
        pass


class DepartmentsHandlers(IDepartmentsHandlers):
    def __init__(self, getting_service: IGettingService):
        self.getting_service = getting_service

    def get_departments(self, request: HttpRequest) -> Iterable[DepartmentOut]:
        return self.getting_service.get_many_department_out()


class DepartmentHandlers(IDepartmentHandlers):
    def __init__(self, getting_service: IGettingService):
        self.getting_service = getting_service

    def get_department(self, request: HttpRequest, department_id: int = Path(...)) -> DepartmentOut:
        department_out = self.getting_service.try_get_one_department_out(department_id)

        if not department_out:
            raise NotFoundError()

        return department_out
