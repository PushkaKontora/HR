from typing import Iterable

from django.http import HttpRequest
from ninja import Path

from api.internal.v1.departments.domain.entities import DepartmentOut
from api.internal.v1.departments.presentation.routers import IDepartmentHandlers, IDepartmentsHandlers


class DepartmentsHandlers(IDepartmentsHandlers):
    def get_departments(self, request: HttpRequest) -> Iterable[DepartmentOut]:
        pass


class DepartmentHandlers(IDepartmentHandlers):
    def get_department(
        self, request: HttpRequest, department_id: int = Path(...)
    ) -> DepartmentOut:
        pass
