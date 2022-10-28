from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.v1.departments.presentation.handlers import DepartmentHandlers, DepartmentsHandlers
from api.internal.v1.departments.presentation.routers import DepartmentRouter, DepartmentsRouter


class DepartmentsContainer(containers.DeclarativeContainer):
    department_handlers = providers.Singleton(DepartmentHandlers)
    departments_handlers = providers.Singleton(DepartmentsHandlers)

    department_router = providers.Singleton(DepartmentRouter, department_handlers=department_handlers)
    departments_router = providers.Singleton(
        DepartmentsRouter, department_router=department_router, departments_handlers=departments_handlers
    )


def register_departments_api(base: NinjaAPI) -> None:
    container = DepartmentsContainer()

    base.add_router("/departments", container.departments_router())
