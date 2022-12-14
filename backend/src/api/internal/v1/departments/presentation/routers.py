from abc import ABC, abstractmethod
from typing import Iterable, List

from django.http import HttpRequest
from ninja import Path, Router

from api.internal.responses import MessageResponse
from api.internal.v1.departments.domain.entities import DepartmentOut

DEPARTMENTS_TAG = "departments"


class IDepartmentsHandlers(ABC):
    @abstractmethod
    def get_departments(self, request: HttpRequest) -> Iterable[DepartmentOut]:
        pass


class IDepartmentHandlers(ABC):
    @abstractmethod
    def get_department(self, request: HttpRequest, department_id: int = Path(...)) -> DepartmentOut:
        pass


class DepartmentsRouter(Router):
    def __init__(self, department_router: Router, departments_handlers: IDepartmentsHandlers):
        super(DepartmentsRouter, self).__init__(tags=[DEPARTMENTS_TAG])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=departments_handlers.get_departments,
            response={200: List[DepartmentOut]},
        )

        self.add_router("/{int:department_id}", department_router)


class DepartmentRouter(Router):
    def __init__(self, department_handlers: IDepartmentHandlers):
        super(DepartmentRouter, self).__init__(tags=[DEPARTMENTS_TAG])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=department_handlers.get_department,
            response={200: DepartmentOut, 404: MessageResponse},
        )
